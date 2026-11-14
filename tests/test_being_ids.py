"""Sibling beings must not share an id (they did when spawned in the same second)."""

from waft.being import BeingSystem


def test_siblings_spawned_together_get_distinct_ids(tmp_path):
    system = BeingSystem(project_path=tmp_path)
    parent = system.spawn_being(reality_id="test-reality")

    siblings = [
        system.spawn_being(reality_id="test-reality", parent_being_id=parent.being_id)
        for _ in range(8)
    ]

    ids = [b.being_id for b in siblings]
    assert len(set(ids)) == len(ids), ids
    assert parent.being_id not in ids
