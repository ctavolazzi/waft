import random
import tempfile
from pathlib import Path

import pytest

from waft.core.meme_generator import MemeGenerator, MemeRequest


def test_seeded_mixed_mode_is_deterministic(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="ship it", mode="mixed")

    first = generator._choose_style(request, random.Random(42))
    second = generator._choose_style(request, random.Random(42))

    assert first == second


def test_template_mode_uses_template_styles(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="template test", mode="template")

    style = generator._choose_style(request, random.Random(7))
    template_styles = {template.style for template in generator.templates}

    assert style in template_styles


def test_cooking_mode_uses_template_styles(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="kitchen test", mode="cooking")

    style = generator._choose_style(request, random.Random(9))
    template_styles = {template.style for template in generator.templates}

    assert style in template_styles


def test_recipe_selection_applies_recipe_style(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="chef time", recipe="containment_chowder")

    style = generator._choose_style(request, random.Random(1))
    assert style == "motivational"


def test_url_safety_blocks_localhost(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="unsafe", image_url="http://localhost/bad.jpg")

    with pytest.raises(ValueError, match="URL blocked by Bouncer"):
        generator.generate(request)


def test_ffmpeg_command_construction_has_expected_shape(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="make it loud", top_text="TOP", bottom_text="BOTTOM")

    command = generator._build_ffmpeg_command(
        "top_bottom", Path("/tmp/input.jpg"), Path("/tmp/out.jpg"), request
    )

    assert command[0] == "ffmpeg"
    assert "-vf" in command
    assert "/tmp/out.jpg" in command


def test_ffmpeg_command_uses_configured_binary(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    generator.ffmpeg_bin = "ffmpeg-custom"
    request = MemeRequest(prompt="custom bin")

    command = generator._build_ffmpeg_command(
        "top_bottom", Path("/tmp/input.jpg"), Path("/tmp/out.jpg"), request
    )

    assert command[0] == "ffmpeg-custom"


def test_topical_without_config_falls_back_to_source_url(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="topic", topical=True)

    source = generator._resolve_topical_source("https://picsum.photos/1280/720", request, random.Random(1))

    assert source == "https://picsum.photos/1280/720"


def test_fit_text_block_wraps_and_clamps_lines(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    long_text = " ".join(["absurdlylongmemephrase"] * 80)

    fitted, font = generator._fit_text_block(
        long_text,
        max_width_px=1180,
        min_font=28,
        max_font=62,
        max_lines=3,
    )

    lines = fitted.split("\n")
    assert 1 <= len(lines) <= 3
    assert 28 <= font <= 62
    assert all(line.strip() for line in lines)


def test_ffmpeg_filters_include_canvas_normalization_and_box(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="text readability test", top_text="TOP", bottom_text="BOTTOM")

    command = generator._build_ffmpeg_command(
        "top_bottom", Path("/tmp/input.jpg"), Path("/tmp/out.jpg"), request
    )
    vf = command[command.index("-vf") + 1]

    assert "scale=1280:720:force_original_aspect_ratio=decrease" in vf
    assert "pad=1280:720:(ow-iw)/2:(oh-ih)/2:black" in vf
    assert "box=1:boxcolor=black@0.45:boxborderw=12" in vf


@pytest.mark.parametrize(
    ("style_name", "expected_fragments"),
    [
        (
            "top_bottom",
            [
                "scale=1280:720:force_original_aspect_ratio=decrease",
                "pad=1280:720:(ow-iw)/2:(oh-ih)/2:black",
                "drawtext=text=",
            ],
        ),
        (
            "top_band",
            [
                "drawbox=x=0:y=0:w=w:h=h*0.22:color=white:t=fill",
                "borderw=2:bordercolor=white",
                "box=1:boxcolor=black@0.45:boxborderw=12",
            ],
        ),
        (
            "motivational",
            [
                "pad=1360:900:(ow-iw)/2:40:black",
                "x=(w-text_w)/2:y=745",
                "x=(w-text_w)/2:y=815",
            ],
        ),
    ],
)
def test_ffmpeg_filter_chain_is_normalized_for_all_styles(
    temp_project_path, style_name, expected_fragments
):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(
        prompt="style regression",
        top_text="TOP: WITH COLON",
        bottom_text="BOTTOM'S QUOTE",
        title="TITLE: WITH COLON",
        subtitle="SUBTITLE'S QUOTE",
    )

    command = generator._build_ffmpeg_command(
        style_name, Path("/tmp/input.jpg"), Path("/tmp/out.jpg"), request
    )
    vf = command[command.index("-vf") + 1]

    assert "\n" not in vf
    assert ",," not in vf
    for fragment in expected_fragments:
        assert fragment in vf


def test_generate_cleans_up_temp_source_file(temp_project_path, monkeypatch):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="cleanup test", output=str(temp_project_path / "out.jpg"))
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    tmp.write(b"fake-image")
    tmp.close()
    temp_image_path = Path(tmp.name)

    def fake_download(_url: str):
        return temp_image_path

    def fake_run(cmd, capture_output, text):
        out_path = Path(cmd[-1])
        out_path.write_bytes(b"rendered")
        return type("Res", (), {"returncode": 0, "stderr": "", "stdout": ""})()

    monkeypatch.setattr(generator, "_download_image", fake_download)
    monkeypatch.setattr("waft.core.meme_generator.subprocess.run", fake_run)
    generated = generator.generate(request)
    assert generated.exists()
    assert not temp_image_path.exists()


def test_generate_fails_with_helpful_error_when_ffmpeg_missing(temp_project_path, monkeypatch):
    generator = MemeGenerator(project_path=temp_project_path)
    generator.ffmpeg_bin = "ffmpeg-definitely-missing"
    request = MemeRequest(prompt="missing ffmpeg", output=str(temp_project_path / "out.jpg"))
    called = {"download": False}

    def fake_download(_url: str):
        called["download"] = True
        return Path("/tmp/should-not-be-used.jpg")

    monkeypatch.setattr(generator, "_download_image", fake_download)
    with pytest.raises(RuntimeError, match="WAFT_FFMPEG_BIN"):
        generator.generate(request)
    assert called["download"] is False


def test_generate_rejects_unsupported_backend_before_download(temp_project_path, monkeypatch):
    generator = MemeGenerator(project_path=temp_project_path)
    generator.backend = "pillow"
    request = MemeRequest(prompt="unsupported backend")
    called = {"download": False}

    def fake_download(_url: str):
        called["download"] = True
        return Path("/tmp/should-not-be-used.jpg")

    monkeypatch.setattr(generator, "_download_image", fake_download)
    with pytest.raises(RuntimeError, match="Unsupported meme backend"):
        generator.generate(request)
    assert called["download"] is False


def test_generate_ffmpeg_non_zero_cleans_up_temp_source_and_raises(temp_project_path, monkeypatch):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="ffmpeg fails", output=str(temp_project_path / "out.jpg"))
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    tmp.write(b"fake-image")
    tmp.close()
    temp_image_path = Path(tmp.name)

    def fake_download(_url: str):
        return temp_image_path

    def fake_run(_cmd, capture_output, text):
        return type("Res", (), {"returncode": 1, "stderr": "boom", "stdout": ""})()

    monkeypatch.setattr(generator, "_download_image", fake_download)
    monkeypatch.setattr("waft.core.meme_generator.subprocess.run", fake_run)

    with pytest.raises(RuntimeError, match="ffmpeg failed: boom"):
        generator.generate(request)
    assert not temp_image_path.exists()


def test_generate_ffmpeg_success_without_output_raises(temp_project_path, monkeypatch):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="missing output", output=str(temp_project_path / "missing.jpg"))
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    tmp.write(b"fake-image")
    tmp.close()
    temp_image_path = Path(tmp.name)

    def fake_download(_url: str):
        return temp_image_path

    def fake_run(_cmd, capture_output, text):
        return type("Res", (), {"returncode": 0, "stderr": "", "stdout": ""})()

    monkeypatch.setattr(generator, "_download_image", fake_download)
    monkeypatch.setattr("waft.core.meme_generator.subprocess.run", fake_run)

    with pytest.raises(RuntimeError, match="no output file"):
        generator.generate(request)
    assert not temp_image_path.exists()


def test_download_image_rejects_non_image_content_type(temp_project_path, monkeypatch):
    generator = MemeGenerator(project_path=temp_project_path)

    class FakeStream:
        headers = {"content-type": "text/plain", "content-length": "5"}

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def raise_for_status(self):
            return None

        def iter_bytes(self):
            yield b"hello"

    monkeypatch.setattr("waft.core.meme_generator.httpx.stream", lambda *args, **kwargs: FakeStream())
    with pytest.raises(ValueError, match="did not return image content"):
        generator._download_image("https://example.com/not-image")


def test_download_image_rejects_oversize_content_length_header(temp_project_path, monkeypatch):
    generator = MemeGenerator(project_path=temp_project_path)

    class FakeStream:
        headers = {"content-type": "image/jpeg", "content-length": str(generator.max_download_bytes + 1)}

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def raise_for_status(self):
            return None

        def iter_bytes(self):
            yield b"small"

    monkeypatch.setattr("waft.core.meme_generator.httpx.stream", lambda *args, **kwargs: FakeStream())
    with pytest.raises(ValueError, match="maximum allowed download size"):
        generator._download_image("https://example.com/too-large-header")


def test_download_image_rejects_oversize_stream_payload(temp_project_path, monkeypatch):
    generator = MemeGenerator(project_path=temp_project_path)

    class FakeStream:
        headers = {"content-type": "image/jpeg"}

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def raise_for_status(self):
            return None

        def iter_bytes(self):
            yield b"a" * (generator.max_download_bytes + 1)

    monkeypatch.setattr("waft.core.meme_generator.httpx.stream", lambda *args, **kwargs: FakeStream())
    with pytest.raises(ValueError, match="maximum allowed download size"):
        generator._download_image("https://example.com/too-large-stream")
