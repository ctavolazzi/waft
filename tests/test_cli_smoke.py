"""Every command the CLI registers must at least print its help.

main.py is the largest module in the package and had no test that touched most of its
commands, so a command that could not even be loaded went unnoticed.
"""

import pytest
import typer
from typer.testing import CliRunner

from waft.main import app

runner = CliRunner()
ROOT = typer.main.get_command(app)


def _command_paths(group, prefix=()):
    """Yield the argument list that reaches every command and sub-command."""
    for name, command in sorted(group.commands.items()):
        path = (*prefix, name)
        yield path
        if hasattr(command, "commands"):
            yield from _command_paths(command, path)


ALL_COMMANDS = list(_command_paths(ROOT))


def test_the_cli_registers_a_plausible_number_of_commands():
    assert len(ROOT.commands) >= 80, sorted(ROOT.commands)


@pytest.mark.parametrize("path", ALL_COMMANDS, ids=[" ".join(p) for p in ALL_COMMANDS])
def test_help_works(path):
    result = runner.invoke(app, [*path, "--help"])
    assert result.exit_code == 0, result.output[-600:]
