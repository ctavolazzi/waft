from __future__ import annotations

import os
import random
import shutil
import subprocess
import tempfile
import textwrap
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import httpx

from .door_guy import Bouncer


@dataclass
class MemeStyle:
    name: str
    description: str


@dataclass
class MemeTemplate:
    name: str
    style: str
    description: str
    category: str = "mainstream"
    featured: bool = False


@dataclass
class MemeRecipe:
    name: str
    style: str
    description: str


@dataclass
class MemeRequest:
    prompt: str
    top_text: str = ""
    bottom_text: str = ""
    title: str = ""
    subtitle: str = ""
    image_url: str = ""
    mode: Literal["mixed", "template", "cooking", "original"] = "mixed"
    style: str = ""
    template: str = ""
    recipe: str = ""
    seed: int | None = None
    temperature: float = 0.7
    top_k: int = 6
    creativity: float = 0.6
    punchiness: float = 0.6
    absurdity: float = 0.4
    topical: bool = False
    output: str = ""


class MemeGenerator:
    def __init__(self, project_path: str | Path | None = None):
        self.project_path = Path(project_path or ".").resolve()
        self.max_download_bytes = 15 * 1024 * 1024  # 15 MB safety cap for remote images
        self.backend = os.getenv("WAFT_MEME_BACKEND", "ffmpeg").strip().lower() or "ffmpeg"
        self.ffmpeg_bin = os.getenv("WAFT_FFMPEG_BIN", "ffmpeg").strip() or "ffmpeg"
        manifest_path = self.project_path / "src" / "waft" / "config" / "port_manifest.example.json"
        self.bouncer = Bouncer.from_manifest_file(manifest_path) if manifest_path.exists() else Bouncer()
        self.styles = [
            MemeStyle("top_bottom", "Classic top and bottom impact-style text overlay."),
            MemeStyle("top_band", "White top caption band with black headline text."),
            MemeStyle("motivational", "Black framed motivational poster with title/subtitle."),
        ]
        self.templates = [
            MemeTemplate(
                "drake",
                "top_bottom",
                "Two-panel reject/approve top-bottom format.",
                category="mainstream",
                featured=True,
            ),
            MemeTemplate(
                "distracted_boyfriend",
                "top_bottom",
                "Three-subject labelable reaction scene.",
                category="mainstream",
                featured=True,
            ),
            MemeTemplate(
                "expanding_brain",
                "top_bottom",
                "Escalating idea ladder for contrast humor.",
                category="mainstream",
                featured=True,
            ),
            MemeTemplate(
                "inspiring_poster",
                "motivational",
                "Motivational poster format with title.",
                category="mainstream",
                featured=True,
            ),
            MemeTemplate(
                "two_buttons",
                "top_bottom",
                "Choice paralysis split-panel format.",
                category="mainstream",
                featured=True,
            ),
            MemeTemplate(
                "change_my_mind",
                "top_band",
                "Contrarian table sign hot-take format.",
                category="mainstream",
                featured=True,
            ),
            MemeTemplate(
                "woman_yelling_cat",
                "top_bottom",
                "Argument vs deadpan reaction split format.",
                category="mainstream",
                featured=True,
            ),
            MemeTemplate(
                "gru_plan",
                "top_bottom",
                "Four-step plan reveal punchline format.",
                category="mainstream",
                featured=True,
            ),
            MemeTemplate(
                "one_does_not_simply",
                "top_band",
                "Reaction macro format for impossible tasks.",
                category="mainstream",
            ),
            MemeTemplate(
                "success_kid",
                "top_bottom",
                "Tiny win celebration impact caption format.",
                category="mainstream",
            ),
            MemeTemplate(
                "ancient_aliens",
                "top_band",
                "Conspiracy explanation macro format.",
                category="mainstream",
            ),
            MemeTemplate(
                "left_exit_12_off_ramp",
                "top_bottom",
                "Sudden chaotic decision fork format.",
                category="mainstream",
            ),
            MemeTemplate(
                "waft_oracle",
                "motivational",
                "WAFT-native oracle prophecy card format.",
                category="waft-native",
            ),
            MemeTemplate(
                "containment_alert",
                "top_band",
                "WAFT containment incident banner format.",
                category="waft-native",
            ),
            MemeTemplate(
                "chef_waft_special",
                "top_bottom",
                "Kitchen-branded WAFT cooking meme format.",
                category="waft-native",
            ),
        ]
        self.recipes = [
            MemeRecipe("burnt_ember", "top_bottom", "Spicy two-line roast format."),
            MemeRecipe("midnight_braise", "top_band", "Top-plated headline with dark aftertaste."),
            MemeRecipe("containment_chowder", "motivational", "Containment poster with ominous garnish."),
            MemeRecipe("chaos_reduction", "top_bottom", "Fast chaos-to-order contrast punchline."),
            MemeRecipe("forbidden_frittata", "top_band", "Classified headline with dramatic footer."),
            MemeRecipe("facility_feast", "motivational", "Site report poster built for incident lore."),
        ]

    def list_styles(self) -> list[MemeStyle]:
        return list(self.styles)

    def list_templates(self) -> list[MemeTemplate]:
        return list(self.templates)

    def list_featured_templates(self) -> list[MemeTemplate]:
        featured = [template for template in self.templates if template.featured]
        if featured:
            return featured
        return list(self.templates[:8])

    def list_recipes(self) -> list[MemeRecipe]:
        return list(self.recipes)

    def generate(self, request: MemeRequest) -> Path:
        rng = random.Random(request.seed if request.seed is not None else time.time_ns())
        source_url = request.image_url.strip() or "https://picsum.photos/1280/720"
        source_url = self._resolve_topical_source(source_url, request, rng)
        decision = self.bouncer.inspect_url(source_url)
        if not decision.allowed:
            raise ValueError(f"URL blocked by Bouncer: {decision.reason}")

        tuned_request = self._apply_tuning(request, rng)
        style_name = self._choose_style(request, rng)
        self._ensure_backend_supported()
        self._ensure_ffmpeg_available()
        image_path = self._download_image(source_url)
        output_path = self._resolve_output_path(request.output)
        ffmpeg_command = self._build_ffmpeg_command(style_name, image_path, output_path, tuned_request)
        try:
            try:
                run_result = subprocess.run(ffmpeg_command, capture_output=True, text=True)
            except FileNotFoundError as exc:
                raise RuntimeError(self._ffmpeg_missing_message()) from exc
            if run_result.returncode != 0:
                raise RuntimeError(f"ffmpeg failed: {run_result.stderr.strip() or run_result.stdout.strip()}")
            if not output_path.exists():
                raise RuntimeError("ffmpeg completed but no output file was created")
            return output_path
        finally:
            # Prevent temp-file buildup from repeated generations.
            try:
                image_path.unlink(missing_ok=True)
            except Exception:
                pass

    def _ensure_backend_supported(self) -> None:
        if self.backend == "ffmpeg":
            return
        raise RuntimeError(
            "Unsupported meme backend. Set WAFT_MEME_BACKEND=ffmpeg. "
            "Additional backends are not yet implemented."
        )

    def _ensure_ffmpeg_available(self) -> None:
        if "/" in self.ffmpeg_bin:
            if not Path(self.ffmpeg_bin).expanduser().exists():
                raise RuntimeError(self._ffmpeg_missing_message())
            return
        if shutil.which(self.ffmpeg_bin) is None:
            raise RuntimeError(self._ffmpeg_missing_message())

    def _ffmpeg_missing_message(self) -> str:
        return (
            f"ffmpeg binary '{self.ffmpeg_bin}' not found. Install ffmpeg or set WAFT_FFMPEG_BIN to a valid "
            "binary/path (macOS: `brew install ffmpeg`, Ubuntu: `sudo apt install ffmpeg`)."
        )

    def _choose_style(self, request: MemeRequest, rng: random.Random) -> str:
        if request.style.strip():
            style_name = request.style.strip().lower()
            if style_name in {style.name for style in self.styles}:
                return style_name

        if request.template.strip():
            template_name = request.template.strip().lower()
            for template in self.templates:
                if template.name == template_name:
                    return template.style

        if request.recipe.strip():
            recipe_name = request.recipe.strip().lower()
            for recipe in self.recipes:
                if recipe.name == recipe_name:
                    return recipe.style

        if request.mode in {"template", "cooking"}:
            return rng.choice([template.style for template in self.templates])
        if request.mode == "original":
            return rng.choice(["top_band", "motivational"])
        return rng.choice([style.name for style in self.styles])

    def _resolve_topical_source(
        self, fallback_url: str, request: MemeRequest, rng: random.Random
    ) -> str:
        if not request.topical:
            return fallback_url

        trend_url = os.getenv("WAFT_MEME_TREND_URL", "").strip()
        if not trend_url:
            return fallback_url

        trend_decision = self.bouncer.inspect_url(trend_url)
        if not trend_decision.allowed:
            return fallback_url

        try:
            response = httpx.get(trend_url, timeout=5.0)
            response.raise_for_status()
            text = response.text.strip()
            if text:
                request.prompt = f"{request.prompt} {text[:120]}"
        except Exception:
            return fallback_url

        topical_images = [
            "https://picsum.photos/seed/trending-1/1280/720",
            "https://picsum.photos/seed/trending-2/1280/720",
            "https://picsum.photos/seed/trending-3/1280/720",
        ]
        return rng.choice(topical_images)

    def _download_image(self, image_url: str) -> Path:
        with httpx.stream("GET", image_url, timeout=20.0, follow_redirects=True) as response:
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if content_type and "image" not in content_type:
                raise ValueError("image URL did not return image content")
            content_length = response.headers.get("content-length")
            if content_length:
                try:
                    parsed_length = int(content_length)
                except ValueError:
                    parsed_length = None
                if parsed_length is not None and parsed_length > self.max_download_bytes:
                    raise ValueError("image URL exceeds maximum allowed download size")
                if parsed_length is None:
                    # Keep behavior strict only when parseable and above limit; malformed header is ignored.
                    pass

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            written = 0
            try:
                for chunk in response.iter_bytes():
                    if not chunk:
                        continue
                    written += len(chunk)
                    if written > self.max_download_bytes:
                        raise ValueError("image URL exceeds maximum allowed download size")
                    temp_file.write(chunk)
            except Exception:
                temp_file.close()
                Path(temp_file.name).unlink(missing_ok=True)
                raise
            temp_file.close()
            return Path(temp_file.name)

    def _resolve_output_path(self, output: str) -> Path:
        if output.strip():
            path = Path(output).expanduser().resolve()
            path.parent.mkdir(parents=True, exist_ok=True)
            return path
        auto_name = f"waft_meme_{int(time.time())}.jpg"
        return (self.project_path / auto_name).resolve()

    def _build_ffmpeg_command(
        self, style_name: str, input_path: Path, output_path: Path, request: MemeRequest
    ) -> list[str]:
        top_text, top_size = self._fit_text_block(
            request.top_text or request.prompt.upper(),
            max_width_px=1180,
            min_font=30,
            max_font=62,
            max_lines=3,
        )
        bottom_text, bottom_size = self._fit_text_block(
            request.bottom_text or "WAFT",
            max_width_px=1180,
            min_font=30,
            max_font=62,
            max_lines=3,
        )
        title_text, title_size = self._fit_text_block(
            request.title or request.prompt[:64].upper(),
            max_width_px=1180,
            min_font=28,
            max_font=56,
            max_lines=2,
        )
        subtitle_text, subtitle_size = self._fit_text_block(
            request.subtitle or "generated by waft meme",
            max_width_px=1180,
            min_font=22,
            max_font=34,
            max_lines=3,
        )
        escaped_top = self._escape_drawtext(top_text)
        escaped_bottom = self._escape_drawtext(bottom_text)
        escaped_title = self._escape_drawtext(title_text)
        escaped_subtitle = self._escape_drawtext(subtitle_text)
        escaped_watermark = self._escape_drawtext(
            "Meme Cooked by Chef WAFT · github.com/FogSift/waft"
        )
        watermark_filter = (
            f"drawtext=text='{escaped_watermark}':fontcolor=white@0.06:fontsize=17:"
            "x=w-text_w-14:y=h-th-14"
        )
        normalized_canvas = (
            "scale=1280:720:force_original_aspect_ratio=decrease,"
            "pad=1280:720:(ow-iw)/2:(oh-ih)/2:black,"
        )

        if style_name == "top_band":
            filters = self._normalize_filter_chain(
                (
                f"{normalized_canvas}"
                "drawbox=x=0:y=0:w=w:h=h*0.22:color=white:t=fill,"
                f"drawtext=text='{escaped_top}':fontcolor=black:fontsize={top_size}:"
                "x=(w-text_w)/2:y=26:borderw=2:bordercolor=white,"
                f"drawtext=text='{escaped_bottom}':fontcolor=white:fontsize={bottom_size}:"
                "x=(w-text_w)/2:y=h-th-44:borderw=3:bordercolor=black:"
                "box=1:boxcolor=black@0.45:boxborderw=12,"
                f"{watermark_filter}"
                )
            )
            return [
                self.ffmpeg_bin,
                "-y",
                "-i",
                str(input_path),
                "-vf",
                filters,
                "-q:v",
                "2",
                str(output_path),
            ]

        if style_name == "motivational":
            filters = self._normalize_filter_chain(
                (
                "scale=1280:720:force_original_aspect_ratio=decrease,"
                "pad=1360:900:(ow-iw)/2:40:black,"
                f"drawtext=text='{escaped_title}':fontcolor=white:fontsize={title_size}:"
                "x=(w-text_w)/2:y=745,"
                f"drawtext=text='{escaped_subtitle}':fontcolor=white:fontsize={subtitle_size}:"
                "x=(w-text_w)/2:y=815,"
                f"{watermark_filter}"
                )
            )
            return [
                self.ffmpeg_bin,
                "-y",
                "-i",
                str(input_path),
                "-vf",
                filters,
                "-q:v",
                "2",
                str(output_path),
            ]

        filters = self._normalize_filter_chain(
            (
            f"{normalized_canvas}"
            f"drawtext=text='{escaped_top}':fontcolor=white:fontsize={top_size}:"
            "x=(w-text_w)/2:y=26:borderw=4:bordercolor=black:"
            "box=1:boxcolor=black@0.45:boxborderw=12,"
            f"drawtext=text='{escaped_bottom}':fontcolor=white:fontsize={bottom_size}:"
            "x=(w-text_w)/2:y=h-th-44:borderw=4:bordercolor=black:"
            "box=1:boxcolor=black@0.45:boxborderw=12,"
            f"{watermark_filter}"
            )
        )
        return [
            self.ffmpeg_bin,
            "-y",
            "-i",
            str(input_path),
            "-vf",
            filters,
            "-q:v",
            "2",
            str(output_path),
        ]

    def _normalize_filter_chain(self, filters: str) -> str:
        # Keep a compact one-line filter chain to reduce parser differences across FFmpeg builds.
        compact = "".join(filters.splitlines()).strip()
        while ",," in compact:
            compact = compact.replace(",,", ",")
        return compact.strip(",")

    def _escape_drawtext(self, text: str) -> str:
        return (
            text.replace("\\", "\\\\")
            .replace("\n", "\\n")
            .replace(":", "\\:")
            .replace("'", "\\'")
        )

    def _fit_text_block(
        self,
        text: str,
        max_width_px: int,
        min_font: int,
        max_font: int,
        max_lines: int,
    ) -> tuple[str, int]:
        cleaned = " ".join((text or "").strip().split())
        if not cleaned:
            return "", min_font

        for font_size in range(max_font, min_font - 1, -2):
            approx_char_px = max(1.0, font_size * 0.56)
            wrap_width = max(8, int(max_width_px / approx_char_px))
            lines = textwrap.wrap(cleaned, width=wrap_width, break_long_words=True, break_on_hyphens=False)
            if 1 <= len(lines) <= max_lines:
                return "\n".join(lines), font_size

        # Hard clamp for worst-case text to guarantee bounds.
        approx_char_px = max(1.0, min_font * 0.56)
        wrap_width = max(8, int(max_width_px / approx_char_px))
        lines = textwrap.wrap(cleaned, width=wrap_width, break_long_words=True, break_on_hyphens=False)
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            if lines[-1] and len(lines[-1]) > 1:
                lines[-1] = lines[-1][:-1] + "…"
        return "\n".join(lines), min_font

    def _apply_tuning(self, request: MemeRequest, rng: random.Random) -> MemeRequest:
        # Temperature and tuning knobs control flavor-word injection and emphasis intensity.
        tuned = MemeRequest(**request.__dict__)
        temperature = max(0.0, min(2.0, float(request.temperature)))
        top_k = max(1, int(request.top_k or 1))
        creativity = max(0.0, min(1.0, float(request.creativity)))
        punchiness = max(0.0, min(1.0, float(request.punchiness)))
        absurdity = max(0.0, min(1.0, float(request.absurdity)))

        flavor_pool = [
            "absolutely",
            "chaotic",
            "legendary",
            "unhinged",
            "forbidden",
            "galactic",
            "quantum",
            "extra crispy",
            "plot twist",
            "boss-level",
            "speedrun",
            "mythic",
        ]
        dynamic_k = max(1, min(len(flavor_pool), int(round(top_k * (0.6 + temperature * 0.4)))))
        picked = rng.sample(flavor_pool, k=min(dynamic_k, len(flavor_pool)))
        intensity = int(round((temperature + creativity + punchiness + absurdity) * 2))
        suffix = " ".join(picked[: max(1, min(3 + intensity // 3, len(picked)))])

        if suffix:
            tuned.prompt = f"{tuned.prompt} {suffix}".strip()
        if not tuned.top_text.strip():
            tuned.top_text = tuned.prompt.upper()[:120]
        if not tuned.bottom_text.strip():
            tuned.bottom_text = ("WAFT " + ("!" * max(1, int(round(1 + punchiness * 4))))).strip()
        if absurdity > 0.55 and rng.random() < absurdity:
            tuned.subtitle = (tuned.subtitle or "ANOMALY DETECTED") + " // CHAOS FACTOR HIGH"
        return tuned
