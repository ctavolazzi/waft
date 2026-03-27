import inspect
import json
from pathlib import Path

import typer
from typer.models import OptionInfo

from ..api.routes import meme_lab as meme_lab_route
from ..core.meme_generator import MemeGenerator, MemeRequest

meme_app = typer.Typer(help="Meme kitchen commands")


@meme_app.command("generate")
def meme_generate(
    prompt: str = typer.Argument(..., help="Prompt or concept to meme."),
    top: str = typer.Option("", "--top", help="Top text."),
    bottom: str = typer.Option("", "--bottom", help="Bottom text."),
    title: str = typer.Option("", "--title", help="Poster title for motivational style."),
    subtitle: str = typer.Option("", "--subtitle", help="Poster subtitle for motivational style."),
    image_url: str = typer.Option("", "--image-url", help="Direct source image URL."),
    mode: str = typer.Option("mixed", "--mode", help="mixed|cooking|template|original"),
    style: str = typer.Option("", "--style", help="Override style by name."),
    template: str = typer.Option("", "--template", help="Legacy template name."),
    recipe: str = typer.Option("", "--recipe", help="Cooking recipe name."),
    seed: int | None = typer.Option(None, "--seed", help="Optional deterministic seed."),
    temperature: float = typer.Option(0.9, "--temperature", help="0.0-2.0 randomness temperature."),
    top_k: int = typer.Option(8, "--top-k", help="Top-k flavor token sampling window."),
    creativity: float = typer.Option(0.8, "--creativity", help="0.0-1.0 creativity dial."),
    punchiness: float = typer.Option(0.8, "--punchiness", help="0.0-1.0 punch intensity."),
    absurdity: float = typer.Option(0.55, "--absurdity", help="0.0-1.0 chaos/absurdity dial."),
    topical: bool = typer.Option(False, "--topical", help="Enable optional topical hook mode."),
    config: str = typer.Option("", "--config", help="Optional JSON file with request overrides."),
    output: str = typer.Option("", "--output", "-o", help="Output image file path."),
    path: str = typer.Option(".", "--path", "-p", help="Project path."),
):
    generator = MemeGenerator(project_path=Path(path))

    def _opt(value, default):
        return default if isinstance(value, OptionInfo) else value

    config_value = _opt(config, "")
    config_data: dict = {}
    if str(config_value).strip():
        config_path = Path(str(config_value)).expanduser().resolve()
        if not config_path.exists():
            raise typer.BadParameter(f"config file not found: {config_path}")
        config_data = json.loads(config_path.read_text(encoding="utf-8"))

    merged = {
        "prompt": prompt,
        "top_text": _opt(top, ""),
        "bottom_text": _opt(bottom, ""),
        "title": _opt(title, ""),
        "subtitle": _opt(subtitle, ""),
        "image_url": _opt(image_url, ""),
        "mode": _opt(mode, "mixed"),
        "style": _opt(style, ""),
        "template": _opt(template, ""),
        "recipe": _opt(recipe, ""),
        "seed": _opt(seed, None),
        "temperature": _opt(temperature, 0.9),
        "top_k": _opt(top_k, 8),
        "creativity": _opt(creativity, 0.8),
        "punchiness": _opt(punchiness, 0.8),
        "absurdity": _opt(absurdity, 0.55),
        "topical": _opt(topical, False),
        "output": _opt(output, ""),
    }
    merged.update({k: v for k, v in config_data.items() if k in merged})

    request = MemeRequest(
        prompt=merged["prompt"],
        top_text=merged["top_text"],
        bottom_text=merged["bottom_text"],
        title=merged["title"],
        subtitle=merged["subtitle"],
        image_url=merged["image_url"],
        mode=merged["mode"],  # type: ignore[arg-type]
        style=merged["style"],
        template=merged["template"],
        recipe=merged["recipe"],
        seed=merged["seed"],
        temperature=float(merged["temperature"]),
        top_k=int(merged["top_k"]),
        creativity=float(merged["creativity"]),
        punchiness=float(merged["punchiness"]),
        absurdity=float(merged["absurdity"]),
        topical=bool(merged["topical"]),
        output=merged["output"],
    )
    output_path = generator.generate(request)
    typer.echo(f"Generated meme: {output_path}")


@meme_app.command("styles")
def meme_styles(path: str = typer.Option(".", "--path", "-p", help="Project path.")):
    generator = MemeGenerator(project_path=Path(path))
    for style in generator.list_styles():
        typer.echo(f"{style.name}: {style.description}")


@meme_app.command("templates")
def meme_templates(path: str = typer.Option(".", "--path", "-p", help="Project path.")):
    generator = MemeGenerator(project_path=Path(path))
    for template in generator.list_templates():
        category = getattr(template, "category", "mainstream")
        featured = " featured" if getattr(template, "featured", False) else ""
        typer.echo(
            f"{template.name} ({template.style}, {category}{featured}): {template.description}"
        )


@meme_app.command("cooking")
def meme_cooking(path: str = typer.Option(".", "--path", "-p", help="Project path.")):
    generator = MemeGenerator(project_path=Path(path))
    for recipe in generator.list_recipes():
        typer.echo(f"{recipe.name} ({recipe.style}): {recipe.description}")


@meme_app.command("security-check")
def meme_security_check(path: str = typer.Option(".", "--path", "-p", help="Project path.")):
    generator = MemeGenerator(project_path=Path(path))
    failures = 0

    max_download_bytes = getattr(generator, "max_download_bytes", 0)
    download_ok = isinstance(max_download_bytes, int) and 0 < max_download_bytes <= (15 * 1024 * 1024)
    typer.echo(
        f"{'PASS' if download_ok else 'FAIL'} download_size_cap max_download_bytes={max_download_bytes}"
    )
    if not download_ok:
        failures += 1

    history_limit = getattr(meme_lab_route, "MAX_HISTORY_ENTRIES", 0)
    history_ok = isinstance(history_limit, int) and 0 < history_limit <= 10_000
    typer.echo(f"{'PASS' if history_ok else 'FAIL'} history_retention_limit value={history_limit}")
    if not history_ok:
        failures += 1

    file_policy_source = inspect.getsource(meme_lab_route.get_meme_lab_file)
    file_policy_ok = (
        "_work_efforts" in file_policy_source
        and "reports" in file_policy_source
        and "relative_to(reports_root)" in file_policy_source
        and "file path not permitted" in file_policy_source
    )
    typer.echo(f"{'PASS' if file_policy_ok else 'FAIL'} reports_subtree_file_policy")
    if not file_policy_ok:
        failures += 1

    if failures:
        typer.echo(f"Security check failed ({failures} critical issue(s)).")
        raise typer.Exit(code=1)
    typer.echo("Security check passed.")
