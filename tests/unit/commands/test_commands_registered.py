"""Smoke tests confirming new subcommands are wired into the root app and surface get/list."""

import pytest
from typer.testing import CliRunner

from pokecli.main import app

runner = CliRunner()

NEW_COMMANDS = [
    "egg-group",
    "growth-rate",
    "evolution-trigger",
    "move-damage-class",
    "move-learn-method",
    "version",
    "version-group",
    "machine",
    "pokemon-form",
    "region",
    "location",
    "location-area",
    "generation",
    "pokedex",
    "evolution-chain",
]


def test_root_help_lists_new_commands():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for cmd in NEW_COMMANDS:
        assert cmd in result.stdout, f"missing '{cmd}' in root --help"


@pytest.mark.parametrize("cmd", NEW_COMMANDS)
def test_subcommand_exposes_get_and_list(cmd):
    result = runner.invoke(app, [cmd, "--help"])
    assert result.exit_code == 0, f"`{cmd} --help` failed: {result.output}"
    assert "get" in result.stdout
    assert "list" in result.stdout
