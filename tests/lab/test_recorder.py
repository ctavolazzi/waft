"""The record: a run becomes a hash-chained Logbook that two verifiers can check, and damage shows."""

import json
import shutil

import pytest

from waft.lab import LabConfig, run
from waft.lab.recorder import load_run, record, verify_run, verify_with_node

CONFIG = LabConfig(seed=7, generations=3, population=6, trials=2, agent="scripted")


@pytest.fixture(scope="module")
def result():
    return run(CONFIG)


@pytest.fixture
def recorded(result, tmp_path):
    return record(result, tmp_path / "runs", replay=run(CONFIG), repo=tmp_path)


def test_a_recorded_run_verifies_against_its_head_and_passes(recorded):
    assert recorded.report.ok and recorded.report.clean
    assert recorded.verdicts == {"scoring": "pass", "evolution": "pass"}
    assert recorded.status == "pass"
    assert recorded.report.head == recorded.head
    assert recorded.report.warnings == []  # nothing stored that no record cites


def test_the_second_verifier_agrees(recorded):
    second = verify_with_node(recorded.path, recorded.head)
    if second is None:
        pytest.skip("node is not installed")
    assert second["ok"] is True and second["clean"] is True
    assert second["head"] == recorded.head


def test_reading_the_run_back_gives_what_went_in(result, recorded):
    view = load_run(recorded.path)

    assert view.head == recorded.head and view.closed
    assert view.result["digest"] == result.digest
    assert view.summary == result.summary
    assert view.champion == result.champion
    assert view.events == result.events
    assert len(view.controls) == 3 and all(c["ok"] for c in view.controls)
    assert {b["name"] for b in view.balances} >= {"the same settings give the same result"}
    assert view.status == "pass"


def _copy(recorded, tmp_path, name):
    target = tmp_path / name
    shutil.copytree(recorded.path, target)
    return target


def test_one_flipped_bit_in_a_stored_artefact_is_caught(recorded, tmp_path):
    damaged = _copy(recorded, tmp_path, "flipped")
    victim = max((damaged / "objects").glob("*/*"), key=lambda p: p.stat().st_size)
    data = bytearray(victim.read_bytes())
    data[len(data) // 2] ^= 1
    victim.write_bytes(bytes(data))

    assert "E_OBJ_HASH" in verify_run(damaged, recorded.head).codes()


def test_an_edited_record_is_caught(recorded, tmp_path):
    damaged = _copy(recorded, tmp_path, "edited")
    chain = damaged / "chain.jsonl"
    text = chain.read_text()
    assert '"ok":true' in text
    chain.write_text(text.replace('"ok":true', '"ok":false', 1))

    assert "E_HASH" in verify_run(damaged).codes()


def test_a_dropped_record_is_caught(recorded, tmp_path):
    damaged = _copy(recorded, tmp_path, "dropped")
    lines = (damaged / "chain.jsonl").read_text().splitlines()
    del lines[5]
    (damaged / "chain.jsonl").write_text("\n".join(lines) + "\n")

    assert not verify_run(damaged).ok


def test_a_consistent_log_that_is_not_the_published_one_is_caught(recorded):
    assert verify_run(recorded.path).ok  # consistent on its own
    assert "E_HEAD" in verify_run(recorded.path, "0" * 64).codes()


def test_two_runs_that_disagree_are_recorded_as_a_failed_balance(result, tmp_path):
    other = run(LabConfig(seed=8, generations=3, population=6, trials=2, agent="scripted"))

    recorded = record(result, tmp_path / "runs", replay=other, repo=tmp_path)

    assert recorded.report.ok  # the log is intact: it truthfully records a bad outcome
    assert not recorded.report.clean
    assert "F_RECONCILE" in recorded.report.finding_codes()
    assert recorded.verdicts["evolution"] == "fail"
    assert recorded.status == "fail"


def test_a_broken_control_fails_the_scoring_verdict(result, tmp_path):
    broken = json.loads(json.dumps(result.controls))
    broken[0]["observed"] = "0.54"  # what the gym's own formula would have given a silent agent
    tampered = type(result)(**{**result.__dict__, "controls": broken})

    recorded = record(tampered, tmp_path / "runs", repo=tmp_path)

    assert recorded.verdicts["scoring"] == "fail"
    assert "F_CONTROL" in recorded.report.finding_codes()


def test_the_head_differs_between_recordings_but_the_digest_does_not(result, tmp_path):
    """The head names one recorded run (time, host). The digest names what the loop computed."""
    first = record(result, tmp_path / "a", repo=tmp_path)
    second = record(result, tmp_path / "b", repo=tmp_path)

    assert first.head != second.head
    assert load_run(first.path).result["digest"] == load_run(second.path).result["digest"] == result.digest


def test_a_run_without_a_replay_says_so(result, tmp_path):
    recorded = record(result, tmp_path / "runs", repo=tmp_path)
    notes = [json.loads(line) for line in (recorded.path / "chain.jsonl").read_text().splitlines()]
    assert any(r["kind"] == "note" and "not replayed" in r["data"]["text"] for r in notes)
    assert recorded.status == "pass"


def test_a_folder_that_is_not_a_lab_run_is_refused(tmp_path):
    with pytest.raises(ValueError, match="not a recorded run"):
        load_run(tmp_path)
