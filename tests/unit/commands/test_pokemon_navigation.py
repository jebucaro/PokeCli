"""Smoke tests for pokemon encounters/forms sub-commands wiring."""

from typer.testing import CliRunner

from pokecli.main import app

runner = CliRunner()


def test_pokemon_help_lists_navigation_subcommands():
    result = runner.invoke(app, ["pokemon", "--help"])
    assert result.exit_code == 0
    assert "encounters" in result.stdout
    assert "forms" in result.stdout
    # Existing sub-commands still present
    assert "moves" in result.stdout
    assert "species" in result.stdout
    assert "evolution" in result.stdout


def test_pokemon_encounters_help():
    result = runner.invoke(app, ["pokemon", "encounters", "--help"])
    assert result.exit_code == 0
    assert "name_or_id" in result.stdout.lower() or "NAME_OR_ID" in result.stdout


def test_pokemon_forms_help():
    result = runner.invoke(app, ["pokemon", "forms", "--help"])
    assert result.exit_code == 0
    assert "--no-cache" in result.stdout
    assert "--format" in result.stdout
