import random

import pytest

from waft.core.meme_generator import MemeGenerator, MemeRequest


STYLE_CASES = ["top_bottom", "top_band", "motivational"]  # 3

SEED_CASES = list(range(100, 120))  # 20

TEMPLATE_CASES = [  # 15
    ("drake", "top_bottom"),
    ("distracted_boyfriend", "top_bottom"),
    ("expanding_brain", "top_bottom"),
    ("inspiring_poster", "motivational"),
    ("two_buttons", "top_bottom"),
    ("change_my_mind", "top_band"),
    ("woman_yelling_cat", "top_bottom"),
    ("gru_plan", "top_bottom"),
    ("one_does_not_simply", "top_band"),
    ("success_kid", "top_bottom"),
    ("ancient_aliens", "top_band"),
    ("left_exit_12_off_ramp", "top_bottom"),
    ("waft_oracle", "motivational"),
    ("containment_alert", "top_band"),
    ("chef_waft_special", "top_bottom"),
]

RECIPE_CASES = [  # 6
    ("burnt_ember", "top_bottom"),
    ("midnight_braise", "top_band"),
    ("containment_chowder", "motivational"),
    ("chaos_reduction", "top_bottom"),
    ("forbidden_frittata", "top_band"),
    ("facility_feast", "motivational"),
]

FIT_CASES = [  # 25
    ("ship", 1180, 30, 62, 3),
    ("deploy now", 1180, 30, 62, 3),
    ("incident response protocol", 1180, 30, 62, 3),
    (" ".join(["waft"] * 8), 1180, 30, 62, 3),
    (" ".join(["waft"] * 16), 1180, 30, 62, 3),
    (" ".join(["waft"] * 24), 1180, 30, 62, 3),
    (" ".join(["waft"] * 40), 1180, 30, 62, 3),
    (" ".join(["chaos"] * 50), 1180, 30, 62, 3),
    (" ".join(["containment"] * 60), 1180, 30, 62, 3),
    (" ".join(["determinism"] * 80), 1180, 30, 62, 3),
    ("X" * 20, 1180, 30, 62, 3),
    ("X" * 40, 1180, 30, 62, 3),
    ("X" * 80, 1180, 30, 62, 3),
    ("X" * 120, 1180, 30, 62, 3),
    ("X" * 180, 1180, 30, 62, 3),
    ("top line\nbottom line", 1180, 30, 62, 3),
    ("emoji-like-text :) :(", 900, 28, 58, 3),
    ("mixed CASE sentence for readability", 900, 28, 58, 3),
    ("tight canvas text sample", 640, 24, 48, 3),
    ("tiny canvas stress sample", 420, 20, 42, 2),
    (" ".join(["wrap"] * 30), 420, 20, 42, 2),
    (" ".join(["wrap"] * 60), 420, 20, 42, 2),
    (" ".join(["A"] * 80), 560, 18, 36, 2),
    (" ".join(["B"] * 120), 560, 18, 36, 2),
    (" ".join(["C"] * 180), 560, 18, 36, 2),
]

TUNING_CASES = [  # 20
    (-1.0, 0, -0.5, -0.5, -0.5),
    (0.0, 1, 0.0, 0.0, 0.0),
    (0.2, 2, 0.1, 0.2, 0.3),
    (0.4, 3, 0.2, 0.3, 0.4),
    (0.6, 4, 0.3, 0.4, 0.5),
    (0.8, 5, 0.4, 0.5, 0.55),
    (1.0, 6, 0.5, 0.6, 0.6),
    (1.2, 7, 0.6, 0.7, 0.65),
    (1.4, 8, 0.7, 0.8, 0.7),
    (1.6, 9, 0.8, 0.9, 0.75),
    (1.8, 10, 0.9, 1.0, 0.8),
    (2.0, 11, 1.0, 1.0, 0.85),
    (2.5, 12, 1.2, 1.1, 0.9),
    (3.0, 15, 1.4, 1.2, 0.95),
    (3.5, 20, 1.6, 1.4, 1.0),
    (4.0, 25, 2.0, 2.0, 1.2),
    (0.9, 50, 0.4, 0.0, 0.2),
    (1.1, 100, 0.5, 0.25, 0.2),
    (1.3, 200, 0.6, 0.5, 0.2),
    (1.5, 500, 0.7, 0.75, 0.2),
]

ESCAPE_CASES = [  # 11
    "simple text",
    "has:colon",
    "has'apostrophe",
    "line1\nline2",
    r"windows\path\example",
    "combo: value 'quoted'",
    "multi\nline:with'chars",
    r"backslash\and:semicolon:",
    "emoji-ish <> [] ()",
    "already \\ escaped",
    "final:stress'case\nwith\\all",
]


@pytest.mark.parametrize("style_name", STYLE_CASES)
def test_choose_style_explicit_style_always_wins(temp_project_path, style_name):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="style priority", mode="mixed", style=style_name)
    chosen = generator._choose_style(request, random.Random(11))
    assert chosen == style_name


@pytest.mark.parametrize("seed", SEED_CASES)
def test_choose_style_seeded_mixed_always_returns_known_style(temp_project_path, seed):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="seed matrix", mode="mixed")
    known_styles = {style.name for style in generator.styles}
    chosen = generator._choose_style(request, random.Random(seed))
    assert chosen in known_styles


@pytest.mark.parametrize("template_name,expected_style", TEMPLATE_CASES)
def test_template_name_routes_to_expected_style(temp_project_path, template_name, expected_style):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="template routing", mode="template", template=template_name)
    chosen = generator._choose_style(request, random.Random(21))
    assert chosen == expected_style


@pytest.mark.parametrize("recipe_name,expected_style", RECIPE_CASES)
def test_recipe_name_routes_to_expected_style(temp_project_path, recipe_name, expected_style):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(prompt="recipe routing", mode="cooking", recipe=recipe_name)
    chosen = generator._choose_style(request, random.Random(22))
    assert chosen == expected_style


@pytest.mark.parametrize("text,max_width,min_font,max_font,max_lines", FIT_CASES)
def test_fit_text_block_hard_constraints_hold(
    temp_project_path, text, max_width, min_font, max_font, max_lines
):
    generator = MemeGenerator(project_path=temp_project_path)
    fitted, font_size = generator._fit_text_block(
        text,
        max_width_px=max_width,
        min_font=min_font,
        max_font=max_font,
        max_lines=max_lines,
    )
    lines = fitted.split("\n") if fitted else []
    assert min_font <= font_size <= max_font
    assert 0 < len(lines) <= max_lines
    assert all(line.strip() for line in lines)


@pytest.mark.parametrize("temp,top_k,creativity,punchiness,absurdity", TUNING_CASES)
def test_apply_tuning_clamps_and_populates_fields(
    temp_project_path, temp, top_k, creativity, punchiness, absurdity
):
    generator = MemeGenerator(project_path=temp_project_path)
    original = MemeRequest(
        prompt="matrix",
        temperature=temp,
        top_k=top_k,
        creativity=creativity,
        punchiness=punchiness,
        absurdity=absurdity,
        top_text="",
        bottom_text="",
    )
    tuned = generator._apply_tuning(original, random.Random(77))

    assert tuned is not original
    assert original.prompt == "matrix"
    assert tuned.prompt.startswith("matrix")
    assert tuned.top_text.strip()
    assert tuned.bottom_text.startswith("WAFT ")
    assert tuned.bottom_text.count("!") >= 1


@pytest.mark.parametrize(
    ("punchiness", "expected_bangs"),
    [
        (-3.0, 1),  # clamp to 0.0
        (0.0, 1),
        (0.49, 3),
        (1.0, 5),
        (5.0, 5),  # clamp to 1.0
    ],
)
def test_apply_tuning_explicit_punchiness_clamp_outcomes(
    temp_project_path, punchiness, expected_bangs
):
    generator = MemeGenerator(project_path=temp_project_path)
    tuned = generator._apply_tuning(
        MemeRequest(prompt="clamp", punchiness=punchiness, top_k=1, temperature=0.0),
        random.Random(77),
    )
    assert tuned.bottom_text == "WAFT " + ("!" * expected_bangs)


def test_apply_tuning_high_absurdity_clamp_always_adds_anomaly_suffix(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    tuned = generator._apply_tuning(
        MemeRequest(prompt="clamp", absurdity=99.0, subtitle="BASE"),
        random.Random(77),
    )
    assert tuned.subtitle.endswith("// CHAOS FACTOR HIGH")


def test_apply_tuning_low_absurdity_clamp_never_adds_anomaly_suffix(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    tuned = generator._apply_tuning(
        MemeRequest(prompt="clamp", absurdity=-5.0, subtitle="BASE"),
        random.Random(77),
    )
    assert tuned.subtitle == "BASE"


def test_choose_style_invalid_inputs_fall_back_to_mode_default_space(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(
        prompt="fallback",
        mode="mixed",
        style="not-a-style",
        template="not-a-template",
        recipe="not-a-recipe",
    )
    chosen = generator._choose_style(request, random.Random(41))
    assert chosen in {style.name for style in generator.styles}


def test_choose_style_invalid_inputs_in_original_mode_fall_back_to_original_pool(temp_project_path):
    generator = MemeGenerator(project_path=temp_project_path)
    request = MemeRequest(
        prompt="fallback",
        mode="original",
        style="not-a-style",
        template="not-a-template",
        recipe="not-a-recipe",
    )
    chosen = generator._choose_style(request, random.Random(41))
    assert chosen in {"top_band", "motivational"}


@pytest.mark.parametrize("raw_text", ESCAPE_CASES)
def test_escape_drawtext_removes_raw_newlines_and_escapes_control_chars(temp_project_path, raw_text):
    generator = MemeGenerator(project_path=temp_project_path)
    escaped = generator._escape_drawtext(raw_text)

    assert "\n" not in escaped
    if ":" in raw_text:
        assert r"\:" in escaped
    if "'" in raw_text:
        assert r"\'" in escaped
    if "\\" in raw_text:
        assert r"\\" in escaped
