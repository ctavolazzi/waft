"""Turn a recorded run into something to show: a card, a short video, a replay page.

    card.png      1080 x 1350, one idea: where the best fitness started and where it ended
    replay.mp4    1080 x 1920, the family tree growing generation by generation (needs ffmpeg)
    replay.gif    the same, smaller, when ffmpeg is not installed
    replay.html   a self-contained page with the tree, the numbers and how to verify them

Every number drawn here is read from the recorded run, and every image says who the agents
were. A card made from simulated agents says so in the same type as everything else.

The pictures are drawn with Pillow alone, so `waft lab share` works wherever WAFT does.
"""

from __future__ import annotations

import html
import json
import shutil
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .recorder import RunView

FONTS = Path(__file__).resolve().parent / "assets" / "fonts"
FONT_FILES = {
    "display": FONTS / "InterDisplay-ExtraBold.otf",
    "text": FONTS / "Inter-Medium.otf",
    "mono": FONTS / "JetBrainsMono-Medium.ttf",
}
TAGLINE = ("Don't just build agents.", "Breed them.")  # the README's own first line

BG = (11, 13, 16)
PANEL = (19, 23, 28)
RULE = (38, 44, 52)
INK = (242, 240, 234)
MUTED = (146, 152, 162)
FAINT = (86, 93, 104)
AMBER = (245, 165, 36)
AMBER_HOT = (255, 201, 92)
COLD = (62, 72, 86)
DEAD = (196, 82, 70)

SS = 2  # every picture is drawn at twice its size and scaled down, which smooths edges


@lru_cache(maxsize=64)
def _font(key: str, px: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_FILES[key]), px)


def _mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = min(1.0, max(0.0, t))
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))  # type: ignore[return-value]


def fitness_colour(f: float) -> tuple[int, int, int]:
    """Cold slate at 0, amber at 1. One hue, so the picture reads as "warmer is fitter"."""
    return _mix(COLD, AMBER, max(0.0, min(1.0, f)) ** 1.6)


def _ease(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


DESIGN_WIDTH = 1080  # every layout below is written for a canvas this wide


class Pen:
    """A canvas addressed in design units (1080 wide, whatever the output size), drawn at SS times the output size."""

    def __init__(self, width: int, height: int) -> None:
        self.out = (width, height)
        self.k = SS * width / DESIGN_WIDTH  # design units to drawn pixels
        self.width, self.height = DESIGN_WIDTH, height * DESIGN_WIDTH / width
        self.img = Image.new("RGB", (width * SS, height * SS), BG)
        self.d = ImageDraw.Draw(self.img, "RGBA")

    @staticmethod
    def _rgba(colour: tuple[int, ...], alpha: float = 1.0) -> tuple[int, int, int, int]:
        return (colour[0], colour[1], colour[2], round(255 * min(1.0, max(0.0, alpha))))

    def text_width(self, s: str, key: str, size: float, tracking: float = 0.0) -> float:
        f = _font(key, max(1, round(size * self.k)))
        return (f.getlength(s) + tracking * self.k * max(0, len(s) - 1)) / self.k

    def text(self, x: float, y: float, s: str, key: str, size: float, colour: tuple[int, ...],
             anchor: str = "la", alpha: float = 1.0, tracking: float = 0.0, over: tuple[int, int, int] = BG) -> None:
        """Pillow does not alpha-blend text, so a faded word is drawn in a colour mixed toward what is under it."""
        if alpha <= 0.004:
            return
        f = _font(key, max(1, round(size * self.k)))
        fill = _mix(over, colour[:3], alpha)
        if not tracking:
            self.d.text((x * self.k, y * self.k), s, font=f, fill=fill, anchor=anchor)
            return
        total = self.text_width(s, key, size, tracking)
        cx = x - (total if anchor[0] == "r" else total / 2 if anchor[0] == "m" else 0)
        for ch in s:
            self.d.text((cx * self.k, y * self.k), ch, font=f, fill=fill, anchor="l" + anchor[1])
            cx += f.getlength(ch) / self.k + tracking

    def dot(self, x: float, y: float, r: float, fill: tuple[int, ...] | None = None, alpha: float = 1.0,
            outline: tuple[int, ...] | None = None, width: float = 0.0) -> None:
        if r <= 0:
            return
        box = [(x - r) * self.k, (y - r) * self.k, (x + r) * self.k, (y + r) * self.k]
        self.d.ellipse(box, fill=self._rgba(fill, alpha) if fill else None,
                       outline=self._rgba(outline, alpha) if outline else None, width=max(1, round(width * self.k)) if outline else 0)

    def line(self, points: list[tuple[float, float]], colour: tuple[int, ...], width: float, alpha: float = 1.0) -> None:
        if len(points) < 2:
            return
        self.d.line([(x * self.k, y * self.k) for x, y in points], fill=self._rgba(colour, alpha),
                    width=max(1, round(width * self.k)), joint="curve")

    def rect(self, x0: float, y0: float, x1: float, y1: float, fill: tuple[int, ...], radius: float = 0, alpha: float = 1.0) -> None:
        self.d.rounded_rectangle([x0 * self.k, y0 * self.k, x1 * self.k, y1 * self.k], radius=radius * self.k, fill=self._rgba(fill, alpha))

    def image(self) -> Image.Image:
        return self.img.resize(self.out, Image.LANCZOS)


# ---------------------------------------------------------------------- what a run looks like


@dataclass
class Node:
    id: str
    parent: str | None
    fitness: float
    rank: int
    kept: bool
    dead: bool


@dataclass
class Story:
    """The run, reduced to what the pictures draw."""

    generations: list[list[Node]]
    best: list[float]
    mean: list[float]
    lineage: set[tuple[int, str]]  # the champion and its ancestors, as (generation, id)
    label: str
    head: str
    run_id: str
    date: str
    status: str
    population: int
    tasks_per_variant: int
    first_try: tuple[float, float]
    champion_traits: list[str]
    digest: str

    @property
    def last(self) -> int:
        return len(self.generations) - 1


def story_of(view: RunView) -> Story:
    generations: dict[int, list[Node]] = {}
    for e in view.events:
        if e["event"] == "EVAL":
            generations.setdefault(e["generation"], []).append(
                Node(e["id"], e.get("parent"), float(e["fitness"]), int(e["rank"]), bool(e["kept"]), bool(e["dead"]))
            )
    ordered = [sorted(generations[g], key=lambda n: n.rank) for g in sorted(generations)]

    lineage: set[tuple[int, str]] = set()
    current: str | None = ordered[-1][0].id
    for g in range(len(ordered) - 1, -1, -1):
        node = next((n for n in ordered[g] if n.id == current), None)
        if node is None:
            break
        lineage.add((g, node.id))
        current = node.parent

    cfg = view.result["config"]
    return Story(
        generations=ordered,
        best=[float(s["best"]) for s in view.summary],
        mean=[float(s["mean"]) for s in view.summary],
        lineage=lineage,
        label=view.result["label"],
        head=view.head,
        run_id=view.run_id,
        date=view.started[:10],
        status=view.status,
        population=int(cfg["population"]),
        tasks_per_variant=int(cfg["trials"]) * len(view.result["quests"]),
        first_try=(float(view.summary[0]["first_try_rate"]), float(view.summary[-1]["first_try_rate"])),
        champion_traits=list(view.champion.get("traits", [])),
        digest=view.result["digest"],
    )


# ---------------------------------------------------------------------- drawing


def _draw_tree(pen: Pen, s: Story, box: tuple[float, float, float, float], reveal: float) -> None:
    """The family tree: one column per generation, fittest on top, lines from parent to child."""
    x0, y0, x1, y1 = box
    cols = len(s.generations)
    rows = max(len(g) for g in s.generations)
    # Size the dots from the spacing, then pull the grid in so the outer dots (and the glow
    # around the winner's line) stay inside the panel.
    r = max(3.0, min((x1 - x0) / max(1, cols - 1), (y1 - y0) / max(1, rows - 1)) * 0.3)
    inset = r * 1.5
    x0, y0, x1, y1 = x0 + inset, y0 + inset, x1 - inset, y1 - inset
    dx = (x1 - x0) / max(1, cols - 1)
    dy = (y1 - y0) / max(1, rows - 1)
    r = max(3.0, min(dx, dy) * 0.3)

    def at(g: int, rank: int) -> tuple[float, float]:
        return x0 + g * dx, y0 + rank * dy

    where = [{n.id: n for n in gen} for gen in s.generations]

    for layer in ("others", "lineage"):  # the champion's line is drawn last, on top
        for g in range(1, cols):
            u = _ease(reveal - g + 0.35)
            if u <= 0:
                continue
            for n in s.generations[g]:
                parent = where[g - 1].get(n.parent or "")
                if parent is None:
                    continue
                on_line = (g, n.id) in s.lineage and (g - 1, parent.id) in s.lineage
                if on_line != (layer == "lineage"):
                    continue
                ax, ay = at(g - 1, parent.rank)
                bx, by = at(g, n.rank)
                ex, ey = ax + (bx - ax) * u, ay + (by - ay) * u
                if on_line:
                    pen.line([(ax, ay), (ex, ey)], AMBER, max(2.5, r * 0.34))
                else:
                    pen.line([(ax, ay), (ex, ey)], MUTED, max(1.0, r * 0.1), alpha=0.34 if n.kept else 0.16)

    for g in range(cols):
        u = _ease((reveal - g) * 1.6)
        if u <= 0:
            continue
        for n in s.generations[g]:
            x, y = at(g, n.rank)
            size = r * (1.0 if n.kept else 0.66) * (0.4 + 0.6 * u)
            if n.dead:
                pen.dot(x, y, size, fill=BG, outline=DEAD, width=max(1.5, r * 0.14), alpha=u)
                continue
            colour = AMBER_HOT if n.fitness >= 0.9995 else fitness_colour(n.fitness)
            if (g, n.id) in s.lineage:
                pen.dot(x, y, size * 1.5, fill=AMBER, alpha=0.2 * u)
            pen.dot(x, y, size, fill=colour, alpha=u)


def _draw_curve(pen: Pen, s: Story, box: tuple[float, float, float, float], reveal: float) -> None:
    """Best (amber) and mean (grey) fitness per generation, on a 0 to 1 scale."""
    x0, y0, x1, y1 = box
    cols = len(s.best)
    dx = (x1 - x0) / max(1, cols - 1)
    for level in (0.0, 0.5, 1.0):
        y = y1 - (y1 - y0) * level
        pen.line([(x0, y), (x1, y)], RULE, 1.5)
        pen.text(x0 - 14, y, f"{level:g}", "mono", 19, FAINT, anchor="rm")

    def path(values: list[float]) -> list[tuple[float, float]]:
        pts = []
        upto = min(reveal, cols - 1)
        for g in range(cols):
            if g > upto:
                frac = upto - (g - 1)
                if 0 < frac < 1:
                    v = values[g - 1] + (values[g] - values[g - 1]) * frac
                    pts.append((x0 + (g - 1 + frac) * dx, y1 - (y1 - y0) * v))
                break
            pts.append((x0 + g * dx, y1 - (y1 - y0) * values[g]))
        return pts

    pen.line(path(s.mean), MUTED, 3, alpha=0.75)
    best = path(s.best)
    pen.line(best, AMBER, 5)
    if best:
        pen.dot(best[-1][0], best[-1][1], 9, fill=AMBER_HOT)


def _draw_legend(pen: Pen, x: float, y: float) -> None:
    """What the marks in the tree mean, in the marks themselves."""
    size, colour = 19, FAINT

    def word(text: str, at: float) -> float:
        pen.text(at, y, text, "mono", size, colour, anchor="lm")
        return at + pen.text_width(text, "mono", size) + 30

    pen.dot(x + 8, y, 8, fill=fitness_colour(0.8))
    x = word("kept", x + 24)
    pen.dot(x + 5, y, 5, fill=fitness_colour(0.8))
    x = word("replaced", x + 18)
    pen.dot(x + 7, y, 7, fill=BG, outline=DEAD, width=2)
    x = word("scored below 0.5", x + 22)
    pen.line([(x, y), (x + 30, y)], AMBER, 4)
    word("the winner's line", x + 40)


def _fit_size(pen: Pen, text: str, key: str, max_width: float, start: float) -> float:
    size = start
    while size > 24 and pen.text_width(text, key, size) > max_width:
        size -= 4
    return size


def render(s: Story, width: int, height: int, reveal: float | None = None, closing: float = 1.0) -> Image.Image:
    """One picture of the run.

    `reveal` is how many generations are showing (None means all of them, the finished
    state). `closing` fades the final headline and the proof lines in (0 to 1).
    """
    pen = Pen(width, height)
    width, height = pen.width, pen.height  # from here on, design units
    done = reveal is None
    shown = float(s.last) if done else max(0.0, min(float(s.last), reveal))
    m = round(width * 0.067)  # the margin
    tall = height / width > 1.5

    # ---- header
    y = m
    pen.text(m, y, "WAFT LAB", "mono", 26, AMBER, tracking=5)
    pen.text(width - m, y, s.date, "mono", 26, FAINT, anchor="ra")
    y += 62 if not tall else 96

    final_headline = f"{s.best[0]:.2f} → {s.best[-1]:.2f}"
    head_size = _fit_size(pen, final_headline, "display", width - 2 * m, 196)
    if done or closing > 0 and reveal is not None and reveal >= s.last:
        a = closing if not done else 1.0
        pen.text(m - 4, y, final_headline, "display", head_size, INK, alpha=a)
        sub = f"best fitness, generation 0 to {s.last}"
        if a < 1:  # cross-fade from the running counter
            g = int(shown)
            pen.text(m - 4, y, f"{s.best[g]:.2f}", "display", head_size, INK, alpha=1 - a)
    else:
        g = int(shown)
        pen.text(m - 4, y, f"{s.best[g]:.2f}", "display", head_size, INK)
        sub = f"best fitness, generation {g} of {s.last}"
    y += head_size * 1.08
    pen.text(m, y, sub, "text", 38, MUTED)
    y += 86 if not tall else 120

    # ---- footer (laid out from the bottom up, so the pictures get what is left)
    fy = height - m
    pen.text(m, fy, " ".join(TAGLINE), "text", 30, INK, anchor="ls")
    if s.status != "pass":
        pen.text(width - m, fy, f"RUN VERDICT: {s.status.upper()}", "mono", 24, DEAD, anchor="rs")
    fy -= 62
    pen.line([(m, fy), (width - m, fy)], RULE, 2)
    proof_alpha = 1.0 if done else closing
    fy -= 26
    head_size_px = _fit_size(pen, s.head, "mono", width - 2 * m, 22)
    pen.text(m, fy, s.head, "mono", head_size_px, FAINT, anchor="ls", alpha=proof_alpha)
    fy -= 34
    pen.text(m, fy, "Every step is in a hash-chained log. Check it:  waft lab verify", "text", 25, MUTED, anchor="ls", alpha=proof_alpha)
    fy -= 50
    pen.text(m, fy, s.label, "mono", 25, INK, anchor="ls")
    facts = f"{s.population} variants per generation  ·  {s.tasks_per_variant} scored tasks each"
    fy -= 42
    pen.text(m, fy, facts, "mono", 25, MUTED, anchor="ls")
    fy -= 64

    # ---- the pictures share what is left
    top, bottom = y, fy
    curve_h = (bottom - top) * (0.27 if not tall else 0.24)
    gap = 78 if not tall else 84
    tree_box = (m + 26, top + 22, width - m - 26, bottom - curve_h - gap - 22)
    panel_bottom = bottom - curve_h - gap
    pen.rect(m, top, width - m, panel_bottom, PANEL, radius=28)
    _draw_tree(pen, s, tree_box, float(s.last) + 2 if done else shown)
    _draw_legend(pen, m + 6, panel_bottom + (32 if not tall else 34))
    curve_box = (m + 40, bottom - curve_h, width - m - 10, bottom - 34)
    _draw_curve(pen, s, curve_box, float(s.last) if done else shown)
    pen.text(curve_box[0], bottom - 2, "generation 0", "mono", 19, FAINT, anchor="ls")
    pen.text(curve_box[2], bottom - 2, f"generation {s.last}", "mono", 19, FAINT, anchor="rs")
    legend_x = (curve_box[0] + curve_box[2]) / 2
    pen.text(legend_x - 12, bottom - 2, "best", "mono", 19, AMBER, anchor="rs")
    pen.text(legend_x + 12, bottom - 2, "mean", "mono", 19, MUTED, anchor="ls")
    return pen.image()


def render_title(width: int, height: int, t: float) -> Image.Image:
    """The opening frame of the video: the tagline, two lines, fading in one after the other."""
    pen = Pen(width, height)
    width, height = pen.width, pen.height  # design units
    m = round(width * 0.067)
    size = _fit_size(pen, TAGLINE[0], "display", width - 2 * m, 104)
    y = height * 0.4
    pen.text(m, y, TAGLINE[0], "display", size, INK, alpha=_ease(t * 2.2))
    pen.text(m, y + size * 1.2, TAGLINE[1], "display", size, AMBER, alpha=_ease(t * 2.2 - 0.9))
    pen.text(m, m, "WAFT LAB", "mono", 26, AMBER, tracking=5)
    return pen.image()


# ---------------------------------------------------------------------- files


def write_card(s: Story, path: Path, size: tuple[int, int] = (1080, 1350)) -> Path:
    render(s, *size).save(path, "PNG", optimize=True)
    return path


def video_frames(s: Story, size: tuple[int, int], fps: int):
    """Yield the frames of the replay: title, the tree growing, then the finished picture held."""
    width, height = size
    per_generation = max(0.28, min(0.75, 8.0 / (s.last + 1)))
    for i in range(round(1.9 * fps)):
        yield render_title(width, height, i / (1.9 * fps))
    build = round((s.last + 1) * per_generation * fps)
    for i in range(build):
        yield render(s, width, height, reveal=(i / fps) / per_generation, closing=0.0)
    for i in range(round(0.8 * fps)):
        yield render(s, width, height, reveal=float(s.last), closing=_ease(i / (0.8 * fps)))
    final = render(s, width, height)
    for _ in range(round(3.0 * fps)):
        yield final


def write_video(s: Story, path: Path, size: tuple[int, int] = (1080, 1920), fps: int = 30) -> Path | None:
    """H.264 in an MP4, the format every social app takes. Returns None when ffmpeg is not installed."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return None
    proc = subprocess.Popen(
        [ffmpeg, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{size[0]}x{size[1]}",
         "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", str(path)],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None
    try:
        for frame in video_frames(s, size, fps):
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
    except BrokenPipeError:
        pass
    err = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
    if proc.wait() != 0 or not path.exists():
        raise RuntimeError(f"ffmpeg could not write {path.name}: {err[-300:]}")
    return path


def write_gif(s: Story, path: Path, size: tuple[int, int] = (540, 960), fps: int = 12) -> Path:
    """The fallback when there is no ffmpeg: smaller and slower, but plays everywhere."""
    frames = [f.quantize(colors=96, method=Image.Quantize.MEDIANCUT) for f in video_frames(s, size, fps)]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=round(1000 / fps), loop=0, optimize=True)
    return path


def write_replay_page(view: RunView, s: Story, path: Path) -> Path:
    """A page that needs nothing but a browser: the tree, the numbers, and how to check them."""
    data = {
        "generations": [[{"id": n.id, "parent": n.parent, "fitness": n.fitness, "rank": n.rank, "kept": n.kept,
                          "dead": n.dead, "line": (g, n.id) in s.lineage} for n in gen]
                        for g, gen in enumerate(s.generations)],
        "best": s.best, "mean": s.mean,
    }
    rows = "".join(
        f"<tr><td>{r['generation']}</td><td>{r['best']:.2f}</td><td>{r['mean']:.2f}</td><td>{r['worst']:.2f}</td>"
        f"<td>{r['first_try_rate']:.0%}</td><td>{r['dead']}</td></tr>"
        for r in view.summary
    )
    checks = "".join(
        f"<li class='{'ok' if c['ok'] else 'bad'}'><b>{html.escape(c['class'])}</b> {html.escape(c['name'])}</li>"
        for c in view.checks
    )
    controls = "".join(
        f"<li class='{'ok' if c['ok'] else 'bad'}'>{html.escape(c['name'])}: expected {html.escape(c['expected'])}, "
        f"observed {html.escape(c['observed'])}</li>" for c in view.controls
    )
    prompt = view.champion.get("system_prompt")
    page = _PAGE.format(
        title=html.escape(f"WAFT lab run {s.run_id}"),
        headline=f"{s.best[0]:.2f} &rarr; {s.best[-1]:.2f}",
        sub=html.escape(f"best fitness, generation 0 to {s.last}"),
        label=html.escape(s.label),
        facts=html.escape(f"{s.population} variants per generation, {s.tasks_per_variant} scored tasks each, seed {view.result['config']['seed']}"),
        head=html.escape(s.head), digest=html.escape(s.digest), run_id=html.escape(s.run_id),
        status=html.escape(s.status),
        traits=html.escape(", ".join(s.champion_traits)),
        prompt=f"<h2>The champion's system prompt</h2><p class='mono'>{html.escape(prompt)}</p>" if prompt else "",
        rows=rows, checks=checks, controls=controls,
        tagline=html.escape(" ".join(TAGLINE)),
        data=json.dumps(data, separators=(",", ":")),
    )
    path.write_text(page, encoding="utf-8")
    return path


def share(view: RunView, out_dir: Path | str, *, video: bool = True) -> dict[str, Path]:
    """Write every shareable file for a run into `out_dir`. Returns what was written."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    s = story_of(view)
    made: dict[str, Path] = {"card": write_card(s, out / "card.png"), "page": write_replay_page(view, s, out / "replay.html")}
    if video:
        mp4 = write_video(s, out / "replay.mp4")
        if mp4:
            made["video"] = mp4
        else:
            made["gif"] = write_gif(s, out / "replay.gif")
    return made


_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{ --bg:#0b0d10; --panel:#13171c; --rule:#262c34; --ink:#f2f0ea; --muted:#9298a2; --faint:#565d68; --amber:#f5a524; --dead:#c45246; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:17px/1.5 Inter, system-ui, -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width:900px; margin:0 auto; padding:28px 16px 64px; }}
.mono, code, td, th {{ font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace; }}
.eyebrow {{ color:var(--amber); letter-spacing:.22em; font-size:14px; }}
h1 {{ font-size:clamp(56px, 16vw, 132px); line-height:1; margin:18px 0 6px; font-weight:800; letter-spacing:-.02em; }}
h2 {{ font-size:20px; margin:40px 0 10px; }}
.sub {{ color:var(--muted); font-size:20px; margin:0 0 4px; }}
.label {{ margin:14px 0 0; }}
.facts {{ color:var(--muted); margin:2px 0 0; font-size:15px; }}
.panel {{ background:var(--panel); border-radius:18px; padding:14px; margin-top:22px; }}
svg {{ width:100%; height:auto; display:block; }}
button {{ background:var(--amber); color:#14110a; border:0; border-radius:999px; padding:10px 20px; font:inherit; font-weight:700; cursor:pointer; margin-top:14px; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ text-align:right; padding:5px 6px; border-bottom:1px solid var(--rule); white-space:nowrap; }}
th {{ color:var(--muted); font-weight:500; }}
.scroll {{ overflow-x:auto; }}
ul {{ padding-left:20px; margin:6px 0; }}
li.ok::marker {{ color:var(--amber); }} li.bad {{ color:var(--dead); }}
.hash {{ word-break:break-all; color:var(--muted); font-size:14px; }}
pre {{ background:var(--panel); border-radius:12px; padding:14px; overflow-x:auto; font-size:14px; }}
footer {{ margin-top:48px; color:var(--muted); }}
</style></head><body><main>
<div class="eyebrow mono">WAFT LAB</div>
<h1>{headline}</h1>
<p class="sub">{sub}</p>
<p class="label mono">{label}</p>
<p class="facts mono">{facts}</p>
<div class="panel"><svg id="tree" viewBox="0 0 900 470" role="img" aria-label="Family tree of the run: one column per generation, fittest on top"></svg></div>
<button id="again" type="button">Play again</button>

<h2>Check it yourself</h2>
<p>This run is a hash-chained log. Its last hash, the head, is below. If the log verifies against this head, nothing in it was edited after the run.</p>
<pre>waft lab verify {run_id} --expect-head {head}</pre>
<p class="hash mono">head {head}<br>result digest {digest}</p>
<p>The head names this recorded run. The result digest names what the loop computed: run it again with the same settings and deterministic agents and you get the same digest. Run verdict: <b>{status}</b>.</p>

<h2>The champion</h2>
<p class="mono">{traits}</p>
{prompt}

<h2>Generation by generation</h2>
<div class="scroll"><table><thead><tr><th>gen</th><th>best</th><th>mean</th><th>worst</th><th>first try</th><th>under 0.5</th></tr></thead><tbody>{rows}</tbody></table></div>

<h2>Controls: can the scoring fail, can it pass?</h2>
<ul>{controls}</ul>
<h2>What the run had to earn</h2>
<ul>{checks}</ul>
<footer>{tagline}</footer>
</main>
<script>
const DATA = {data};
const NS = "http://www.w3.org/2000/svg", svg = document.getElementById("tree");
const W = 900, H = 470, PAD = 34, cols = DATA.generations.length, rows = Math.max(...DATA.generations.map(g => g.length));
const dx = (W - 2 * PAD) / Math.max(1, cols - 1), dy = (H - 2 * PAD) / Math.max(1, rows - 1), R = Math.max(3, Math.min(dx, dy) * 0.3);
const at = (g, rank) => [PAD + g * dx, PAD + rank * dy];
const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
const colour = f => f >= 0.9995 ? "rgb(255,201,92)" : "rgb(" + mix([62, 72, 86], [245, 165, 36], Math.pow(Math.max(0, Math.min(1, f)), 1.6)).join(",") + ")";
function el(name, attrs) {{ const e = document.createElementNS(NS, name); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; }}
function draw() {{
  svg.replaceChildren();
  const step = Math.max(160, Math.min(520, 6000 / cols));
  DATA.generations.forEach((gen, g) => {{
    const prev = g ? Object.fromEntries(DATA.generations[g - 1].map(n => [n.id, n])) : {{}};
    gen.forEach(n => {{
      const p = prev[n.parent];
      if (p) {{
        const [ax, ay] = at(g - 1, p.rank), [bx, by] = at(g, n.rank), on = n.line && p.line;
        const l = el("line", {{ x1: ax, y1: ay, x2: bx, y2: by, stroke: on ? "#f5a524" : "#9298a2", "stroke-width": on ? Math.max(2.5, R * 0.34) : 1, opacity: 0 }});
        l.dataset.o = on ? 1 : (n.kept ? 0.34 : 0.16); l.dataset.t = g * step; svg.appendChild(l);
      }}
    }});
  }});
  DATA.generations.forEach((gen, g) => gen.forEach(n => {{
    const [x, y] = at(g, n.rank), r = R * (n.kept ? 1 : 0.66);
    const c = n.dead ? el("circle", {{ cx: x, cy: y, r, fill: "#0b0d10", stroke: "#c45246", "stroke-width": 2, opacity: 0 }})
                     : el("circle", {{ cx: x, cy: y, r, fill: colour(n.fitness), opacity: 0 }});
    c.dataset.o = 1; c.dataset.t = g * step;
    c.appendChild(el("title", {{}})).textContent = "generation " + g + ", fitness " + n.fitness.toFixed(2) + (n.kept ? ", kept" : ", not kept");
    svg.appendChild(c);
  }}));
  for (const e of svg.children) setTimeout(() => {{ e.style.transition = "opacity .35s"; e.setAttribute("opacity", e.dataset.o); }}, +e.dataset.t);
}}
document.getElementById("again").addEventListener("click", draw);
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{ draw(); for (const e of svg.children) e.setAttribute("opacity", e.dataset.o); }} else draw();
</script></body></html>
"""
