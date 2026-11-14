"""The pictures: every number on them comes from the run, and they say who the agents were."""

import re
import shutil

import pytest
from PIL import Image

from waft.lab import LabConfig, run
from waft.lab.recorder import load_run, record
from waft.lab.share import FONT_FILES, TAGLINE, render, share, story_of, video_frames


@pytest.fixture(scope="module")
def view(tmp_path_factory):
    config = LabConfig(seed=7, generations=4, population=6, trials=2, agent="scripted")
    root = tmp_path_factory.mktemp("share")
    return load_run(record(run(config), root / "runs", replay=run(config), repo=root).path)


def test_the_fonts_ship_with_the_package():
    assert all(path.exists() for path in FONT_FILES.values())


def test_the_story_is_read_from_the_run(view):
    s = story_of(view)

    assert s.best == [row["best"] for row in view.summary]
    assert len(s.generations) == 5 and all(len(g) == 6 for g in s.generations)
    assert s.head == view.head and s.label == "simulated agents (scripted fake model)"
    # The winner's line runs from the last generation back to generation 0, one variant per generation.
    assert sorted(g for g, _id in s.lineage) == [0, 1, 2, 3, 4]
    assert (4, view.champion["id"]) in s.lineage


def test_the_card_and_the_page_are_written(view, tmp_path):
    made = share(view, tmp_path, video=False)

    with Image.open(made["card"]) as card:
        assert card.size == (1080, 1350)
        assert len(card.convert("RGB").getcolors(1 << 24)) > 200  # a drawing, not a blank
    page = made["page"].read_text()
    s = story_of(view)
    assert f"{s.best[0]:.2f} &rarr; {s.best[-1]:.2f}" in page
    assert view.head in page and view.result["digest"] in page
    assert "simulated agents (scripted fake model)" in page  # the page says who the agents were
    assert " ".join(TAGLINE).replace("'", "&#x27;") in page
    assert not re.search(r'(src|href)="https?://', page)  # self-contained: nothing is fetched
    assert "—" not in page and "–" not in page


def test_the_card_shows_a_verdict_that_is_not_a_pass(view):
    from dataclasses import replace

    plain = render(story_of(view), 1080, 1350)
    warned = render(replace(story_of(view), status="warn"), 1080, 1350)
    assert plain.tobytes() != warned.tobytes()


def test_the_replay_has_a_title_a_build_and_a_held_ending(view):
    frames = list(video_frames(story_of(view), (270, 480), fps=4))

    assert all(f.size == (270, 480) for f in frames)
    assert frames[-1].tobytes() == frames[-2].tobytes()  # the finished picture is held
    assert frames[0].tobytes() != frames[len(frames) // 2].tobytes() != frames[-1].tobytes()


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg is not installed")
def test_the_video_is_an_h264_mp4(view, tmp_path):
    from waft.lab.share import write_video

    path = write_video(story_of(view), tmp_path / "replay.mp4", size=(270, 480), fps=6)

    assert path is not None and path.stat().st_size > 5_000
    with open(path, "rb") as f:
        assert b"ftyp" in f.read(32)  # an MP4 container


def test_without_ffmpeg_the_replay_is_a_gif(view, tmp_path, monkeypatch):
    import waft.lab.share as share_module

    monkeypatch.setattr(share_module.shutil, "which", lambda _name: None)
    monkeypatch.setattr(share_module, "write_gif", lambda s, path, **_kw: path.write_bytes(b"GIF89a") and path)

    made = share(view, tmp_path, video=True)

    assert "video" not in made and made["gif"].read_bytes() == b"GIF89a"
