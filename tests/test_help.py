"""The command line's own words: --help names the module and shows the developer options, and a missing board
template says how to set the template folder."""

import sys
from pathlib import Path

import pytest

from app.__main__ import main as app_main
from loopgen.__main__ import main as loopgen_main


def help_output(main, monkeypatch, capsys, name):
    monkeypatch.setattr(sys, "argv", [name, "--help"])
    with pytest.raises(SystemExit) as exit_:
        main()
    assert exit_.value.code == 0
    return capsys.readouterr().out


def test_app_help_lists_the_developer_options(monkeypatch, capsys):
    out = help_output(app_main, monkeypatch, capsys, "app")
    assert "usage: python -m app" in out
    for option in ("--templates", "--port", "--browser", "--no-open"):
        assert option in out


def test_loopgen_help_names_the_module(monkeypatch, capsys):
    out = help_output(loopgen_main, monkeypatch, capsys, "loopgen")
    assert "usage: python -m loopgen" in out
    assert "__main__.py" not in out


def test_a_missing_board_template_says_how_to_set_the_folder(monkeypatch, capsys, tmp_path):
    event = Path(__file__).parent.parent / "examples" / "dual-meet" / "event.yaml"
    monkeypatch.setattr(sys, "argv", ["loopgen", str(event), "--check", "--templates", str(tmp_path)])
    assert loopgen_main() == 1
    err = capsys.readouterr().err
    assert f"looked in {tmp_path}" in err
    assert "--templates sets the DisplayLink Plus template folder" in err
