"""Tier 2 tests: agent_protocol — action parsing, prompt assembly, validation."""
import pytest

from agent_protocol import parse_actions, build_system_prompt, build_messages, validate_action


class TestParseActions:
    def test_single_action(self):
        text = """I'll list the files first.

:::action
{"tool": "list_files", "path": "."}
:::

Let me see what's here."""
        actions = parse_actions(text)
        assert len(actions) == 1
        assert actions[0]["tool"] == "list_files"
        assert actions[0]["path"] == "."

    def test_multiple_actions(self):
        text = """Reading two files.

:::action
{"tool": "read_file", "path": "README.md"}
:::

And also:

:::action
{"tool": "read_file", "path": "src/main.py"}
:::

:::action
{"tool": "write_file", "path": "out.txt", "content": "done"}
:::
"""
        actions = parse_actions(text)
        assert len(actions) == 3
        assert actions[2]["tool"] == "write_file"

    def test_no_actions(self):
        text = "Just thinking out loud. No actions needed."
        actions = parse_actions(text)
        assert actions == []

    def test_malformed_json_skipped(self):
        text = """Oops:

:::action
{not valid json}
:::

But this one works:

:::action
{"tool": "list_files", "path": "."}
:::
"""
        actions = parse_actions(text)
        assert len(actions) == 1

    def test_unknown_tool_rejected(self):
        action = {"tool": "exec_code", "path": "evil.py"}
        with pytest.raises(ValueError, match="Unknown tool"):
            validate_action(action)

    def test_valid_tools_accepted(self):
        for tool in ["list_files", "read_file", "write_file", "delete_file"]:
            validate_action({"tool": tool, "path": "."})

    def test_missing_tool_key_rejected(self):
        with pytest.raises(ValueError, match="missing.*tool"):
            validate_action({"path": "."})

    def test_path_with_dotdot_rejected(self):
        with pytest.raises(ValueError, match="(?i)path"):
            validate_action({"tool": "read_file", "path": "../secret"})

    def test_absolute_path_rejected(self):
        with pytest.raises(ValueError, match="path"):
            validate_action({"tool": "read_file", "path": "/etc/passwd"})


class TestBuildSystemPrompt:
    def test_includes_file_tree(self):
        tree = [
            {"name": "index.html", "type": "file", "size": 100},
            {"name": "src", "type": "dir", "size": 0},
        ]
        prompt = build_system_prompt(tree)
        assert "index.html" in prompt
        assert "src" in prompt

    def test_includes_tool_docs(self):
        prompt = build_system_prompt([])
        assert "list_files" in prompt
        assert "write_file" in prompt
        assert ":::action" in prompt

    def test_includes_fogsift_colors(self):
        prompt = build_system_prompt([])
        # FogSift design reference
        assert "#f5" in prompt.lower() or "fogsift" in prompt.lower()


class TestBuildMessages:
    def test_basic_structure(self):
        msgs = build_messages([], "Current files: index.html")
        assert msgs[0]["role"] == "system"
        assert msgs[-1]["role"] == "user"
        assert "index.html" in msgs[-1]["content"]

    def test_includes_history(self):
        history = [
            {"role": "assistant", "content": "I see the files."},
            {"role": "user", "content": "Results: [ok]"},
        ]
        msgs = build_messages(history, "New observation")
        # system + history + observation
        assert len(msgs) == 4

    def test_truncates_long_history(self):
        history = [{"role": "user", "content": f"msg {i}"} for i in range(20)]
        msgs = build_messages(history, "latest")
        # system + last 10 history + observation
        assert len(msgs) <= 12
