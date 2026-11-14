"""`waft lab`: breed variants, put the run on the record, check it, show it."""

from __future__ import annotations

import shutil
import sys
import tempfile
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .agents import model_agents
from .engine import LabConfig, load_dungeon, run
from .fake_model import MODEL_NAME, ScriptedModel, ScriptedServer
from .llm import LLMClient, LLMError, Provider, load_providers
from .recorder import load_run, record, verify_run, verify_with_node

lab_app = typer.Typer(
    help="Directed evolution you can check: breed variants on real tasks, record the run, verify it, share it.",
    no_args_is_help=True,
)
console = Console()

RUNS_DIR = "lab-runs"
MARK = {"pass": "[green]pass[/green]", "warn": "[yellow]warn[/yellow]", "fail": "[red]FAIL[/red]", "skip": "[dim]skip[/dim]"}


def _resolve_run(run: str | None, out: str = RUNS_DIR) -> Path:
    """A run folder, or the newest run under ./lab-runs when none is named."""
    if run and run != "latest":
        path = Path(run)
        if not path.exists() and (Path(out) / run).exists():
            path = Path(out) / run
        if not (path / "chain.jsonl").exists():
            console.print(f"[red]{path} is not a recorded run (no chain.jsonl).[/red]")
            raise typer.Exit(2)
        return path
    runs = sorted((p for p in Path(out).glob("*") if (p / "chain.jsonl").exists()), key=lambda p: p.name)
    if not runs:
        console.print(f"[red]No recorded runs under {out}/. Make one with: waft lab run[/red]")
        raise typer.Exit(2)
    return runs[-1]


@lab_app.command("run")
def run_cmd(
    seed: int = typer.Option(7, "--seed", "-s", help="Same seed, same settings, same result (with simulated agents)"),
    generations: int = typer.Option(12, "--generations", "-g", help="Generations to breed after generation 0"),
    population: int = typer.Option(8, "--population", "-p", help="Variants per generation"),
    trials: int = typer.Option(3, "--trials", "-t", help="Attempts at each quest per variant"),
    agent: str = typer.Option(
        "scripted", "--agent", "-a",
        help="scripted (a scripted fake model, no network), mock (three probabilities), or model (WAFT_LLM_* providers)",
    ),
    out: str = typer.Option(RUNS_DIR, "--out", "-o", help="Folder that holds recorded runs"),
    max_calls: int = typer.Option(2000, "--max-calls", help="Model calls a --agent model run may make before it stops"),
    replay: bool = typer.Option(True, "--replay/--no-replay", help="Run simulated agents twice and require the same result"),
    share: bool = typer.Option(True, "--share/--no-share", help="Also write the card, replay page and video"),
    video: bool = typer.Option(True, "--video/--no-video", help="Include the video (needs ffmpeg; a GIF otherwise)"),
):
    """
    Breed variants on the Jungle Gym's quests and record the run.

    Each variant attempts every quest; the gym validates the answer, lets the agent try to
    repair a bad one, and scores the encounter. The best half carry over, the rest are their
    mutated children. The run is written as a hash-chained Logbook; its head is printed last.
    """
    if agent not in ("scripted", "mock", "model"):
        console.print("[red]--agent must be scripted, mock or model.[/red]")
        raise typer.Exit(2)
    try:
        config = LabConfig(seed=seed, generations=generations, population=population, trials=trials, agent=agent)
    except ValueError as err:
        console.print(f"[red]{err}[/red]")
        raise typer.Exit(2) from None

    agents = None
    if agent == "model":
        try:
            providers = load_providers(warn=lambda m: console.print(f"[yellow]{m}[/yellow]"))
            client = LLMClient(providers, max_calls=max_calls, warn=lambda m: console.print(f"[yellow]{m}[/yellow]"))
        except LLMError as err:
            console.print(f"[red]{err}[/red]")
            console.print("Example, a local model:  WAFT_LLM_BASE_URL=http://localhost:11434/v1 WAFT_LLM_MODEL=llama3.2 waft lab run --agent model")
            raise typer.Exit(2) from None
        agents = model_agents(client)

    console.print(f"\n[bold]WAFT lab[/bold]  seed {seed}, {population} variants, {generations} generations, {trials} trials per quest")

    def progress(row: dict) -> None:
        console.print(f"  generation {row['generation']:>3}   best {row['best']:.2f}   mean {row['mean']:.2f}   below 0.5: {row['dead']}")

    started = time.perf_counter()
    try:
        result = run(config, agents=agents, progress=progress)
    except LLMError as err:
        console.print(f"[red]The run could not start: {err}[/red]")
        raise typer.Exit(1) from None
    console.print(f"  agents: {result.label}")
    second = run(config) if replay and result.agents.get("deterministic") else None
    elapsed = time.perf_counter() - started

    recorded = record(result, out, replay=second, argv=["waft", *sys.argv[1:]] if sys.argv[1:2] == ["lab"] else ["waft", "lab", "run"], repo=Path.cwd())
    console.print(f"\n  scoring controls: {MARK[recorded.verdicts['scoring']]}    evolution: {MARK[recorded.verdicts['evolution']]}    ({elapsed:.1f} s)")
    if result.stopped_early:
        console.print(f"  [yellow]stopped early: {result.stopped_early}[/yellow]")
    console.print(f"  best fitness {result.summary[0]['best']:.2f} -> {result.summary[-1]['best']:.2f}   champion: {', '.join(result.champion['traits'])}")
    console.print(f"  result digest  {result.digest}")
    console.print(f"  run            {recorded.path}")
    console.print(f"  [bold]head           {recorded.head}[/bold]")
    console.print(f"  check it:      waft lab verify {recorded.path} --expect-head {recorded.head}")

    if share:
        from .share import share as write_share

        made = write_share(load_run(recorded.path), recorded.path / "share", video=video)
        for kind, path in made.items():
            console.print(f"  {kind:<14} {path}")
    if not recorded.report.ok or recorded.status == "fail":
        raise typer.Exit(1)


@lab_app.command("verify")
def verify_cmd(
    run: str = typer.Argument(None, help="A run folder (default: the newest under ./lab-runs)"),
    expect_head: str = typer.Option(None, "--expect-head", help="The head hash that was published for this run"),
    node: bool = typer.Option(True, "--node/--no-node", help="Also ask the second verifier (Node), if node is installed"),
):
    """
    Re-derive every hash, flag and verdict of a recorded run. Trusts nothing stored in it.

    Without --expect-head this proves the log is internally consistent. With the head that
    was published when the run was made, it proves the log has not been edited since.
    """
    path = _resolve_run(run)
    report = verify_run(path, expect_head)
    console.print(f"\n[bold]{path.name}[/bold]  {report.records} records, {report.objects} stored artefacts")
    console.print(f"  head {report.head}")
    for p in report.problems:
        console.print(f"  [red]{p['code']}[/red] record {p['seq']}: {p['msg']}")
    for f in report.findings:
        console.print(f"  [yellow]{f['code']}[/yellow] record {f['seq']}: {f['msg']}")
    console.print(f"  python verifier: {'[green]intact[/green]' if report.ok else '[red]NOT INTACT[/red]'}"
                  + ("" if report.clean or not report.ok else "  [yellow](intact, but the run recorded a failed control, balance or handoff)[/yellow]"))
    agreed = True
    if node:
        second = verify_with_node(path, expect_head)
        if second is None:
            console.print("  node verifier:   [dim]skipped (node is not installed)[/dim]")
        else:
            agreed = bool(second.get("ok")) == report.ok
            console.print(f"  node verifier:   {'[green]intact[/green]' if second.get('ok') else '[red]NOT INTACT[/red]'}"
                          + ("" if agreed else "  [red](the two verifiers disagree)[/red]"))
    if not expect_head:
        console.print("  [dim]No --expect-head given: this shows the log is consistent, not that it is the one that was published.[/dim]")
    if not report.ok or not agreed:
        raise typer.Exit(1)


@lab_app.command("show")
def show_cmd(run: str = typer.Argument(None, help="A run folder (default: the newest under ./lab-runs)")):
    """Print what a recorded run says happened: settings, generations, the champion, the checks."""
    view = load_run(_resolve_run(run))
    cfg = view.result["config"]
    console.print(f"\n[bold]{view.run_id}[/bold]  started {view.started}  verdict {MARK[view.status]}")
    console.print(f"  {view.result['label']}")
    console.print(f"  seed {cfg['seed']}, {cfg['population']} variants, {cfg['generations']} generations, {cfg['trials']} trials on {len(view.result['quests'])} quests")

    table = Table(show_edge=False, pad_edge=False)
    for column in ("generation", "best", "mean", "worst", "first-try wins", "below 0.5"):
        table.add_column(column, justify="right")
    for row in view.summary:
        table.add_row(str(row["generation"]), f"{row['best']:.2f}", f"{row['mean']:.2f}", f"{row['worst']:.2f}",
                      f"{row['first_try_rate']:.0%}", str(row["dead"]))
    console.print(table)

    console.print(f"\n  champion {view.champion['id']}: {', '.join(view.champion['traits'])}  (fitness {view.champion['fitness']:.2f})")
    if view.champion.get("system_prompt"):
        console.print(f"  its system prompt: [dim]{view.champion['system_prompt']}[/dim]")
    console.print("\n  controls")
    for c in view.controls:
        console.print(f"    {'[green]held[/green]' if c['ok'] else '[red]BROKE[/red]'}  {c['name']} (expected {c['expected']}, observed {c['observed']})")
    console.print("  checks")
    for c in view.checks:
        console.print(f"    {'[green]ok[/green]  ' if c['ok'] else '[red]NOT[/red] '} [{c['class']}] {c['name']}")
    console.print(f"\n  result digest {view.result['digest']}")
    console.print(f"  head          {view.head}")


@lab_app.command("share")
def share_cmd(
    run: str = typer.Argument(None, help="A run folder (default: the newest under ./lab-runs)"),
    out: str = typer.Option(None, "--out", "-o", help="Where to write (default: the run's own share/ folder)"),
    video: bool = typer.Option(True, "--video/--no-video", help="Include the video (needs ffmpeg; a GIF otherwise)"),
):
    """
    Turn a recorded run into a card (1080 x 1350), a replay page and a short vertical video.

    Every number on them is read from the run, and each one says who the agents were.
    """
    from .share import share as write_share

    path = _resolve_run(run)
    report = verify_run(path)
    if not report.ok:
        console.print("[red]This run does not verify, so nothing was made from it. See: waft lab verify[/red]")
        raise typer.Exit(1)
    made = write_share(load_run(path), Path(out) if out else path / "share", video=video)
    for kind, file in made.items():
        console.print(f"  {kind:<6} {file}")
    if video and "video" not in made:
        console.print("  [dim]ffmpeg is not installed, so the replay is a GIF. Install ffmpeg for an MP4.[/dim]")


@lab_app.command("doctor")
def doctor_cmd():
    """
    Prove the lab works on this machine. Exit code 0 only if every line passes.

    It scores the control agents, runs the loop twice with one seed and once with another,
    records a run, verifies it with both verifiers, damages copies of it three ways to see
    the damage caught, and drives the model path over a real local socket.
    """
    failures: list[str] = []

    def line(ok: bool, what: str, detail: str = "") -> None:
        console.print(f"  {'[green]PASS[/green]' if ok else '[red]FAIL[/red]'}  {what}" + (f"  [dim]{detail}[/dim]" if detail else ""))
        if not ok:
            failures.append(what)

    console.print("\n[bold]WAFT lab doctor[/bold]")
    small = LabConfig(seed=11, generations=4, population=6, trials=2, agent="scripted")
    a, b = run(small), run(small)
    c = run(LabConfig(seed=12, generations=4, population=6, trials=2, agent="scripted"))
    scores = {x["name"]: x for x in a.controls}
    line(all(x["expected"] == x["observed"] for x in a.controls) and len(a.controls) == 3,
         "the scoring can fail and can pass", ", ".join(f"{x['score']:g}" for x in scores.values()))
    line(a.digest == b.digest, "the same seed gives the same result", a.digest[:16])
    line(a.digest != c.digest, "a different seed gives a different result", c.digest[:16])
    bests = [row["best"] for row in a.summary]
    line(all(y >= x for x, y in zip(bests, bests[1:])), "the best score never falls", " ".join(f"{x:.2f}" for x in bests))

    with tempfile.TemporaryDirectory(prefix="waft-lab-doctor-") as tmp:
        root = Path(tmp)
        recorded = record(a, root / "runs", replay=b, argv=["waft", "lab", "doctor"], repo=root)
        line(recorded.report.ok and recorded.report.clean and recorded.status == "pass",
             "a recorded run verifies and passes", f"{recorded.report.records} records")
        second = verify_with_node(recorded.path, recorded.head)
        if second is None:
            console.print("  [dim]SKIP  the second verifier agrees (node is not installed)[/dim]")
        else:
            line(bool(second.get("ok")) and second.get("head") == recorded.head, "the second verifier (Node) agrees")

        def damaged(name: str, harm) -> Path:
            copy = root / name
            shutil.copytree(recorded.path, copy)
            harm(copy)
            return copy

        def flip_object(run_dir: Path) -> None:
            target = max((p for p in (run_dir / "objects").glob("*/*")), key=lambda p: p.stat().st_size)
            data = bytearray(target.read_bytes())
            data[len(data) // 2] ^= 1
            target.write_bytes(bytes(data))

        def edit_chain(run_dir: Path) -> None:
            chain = run_dir / "chain.jsonl"
            chain.write_text(chain.read_text().replace('"ok":true', '"ok":false', 1))

        codes = verify_run(damaged("flipped", flip_object)).codes()
        line("E_OBJ_HASH" in codes, "one flipped bit in a stored artefact is caught", " ".join(codes))
        codes = verify_run(damaged("edited", edit_chain)).codes()
        line("E_HASH" in codes, "an edited record is caught", " ".join(codes))
        line("E_HEAD" in verify_run(recorded.path, "0" * 64).codes(), "a run that is not the published one is caught", "E_HEAD")

        _folder, answers = load_dungeon(small.dungeon)
        model = ScriptedModel(answers, seed=small.seed)
        with ScriptedServer(model) as base_url:
            client = LLMClient([Provider(base_url=base_url, model=MODEL_NAME)], max_calls=400)
            over_http = run(LabConfig(seed=11, generations=1, population=4, trials=1, agent="model"), agents=model_agents(client))
            client.close()
        line(len(model.calls) > 0 and over_http.usage.get("model_calls") == len(model.calls),
             "the model path works over a real socket", f"{len(model.calls)} calls to a scripted model on 127.0.0.1")

        try:
            from .share import share as write_share

            made = write_share(load_run(recorded.path), root / "share", video=False)
            line(made["card"].stat().st_size > 20_000 and made["page"].stat().st_size > 5_000, "a card and a replay page can be drawn")
        except Exception as err:  # noqa: BLE001 (the doctor reports, it does not crash)
            line(False, "a card and a replay page can be drawn", str(err)[:120])

    console.print(f"\n  {'[green]All good.[/green]' if not failures else '[red]' + str(len(failures)) + ' problem(s).[/red]'}")
    if failures:
        raise typer.Exit(1)
