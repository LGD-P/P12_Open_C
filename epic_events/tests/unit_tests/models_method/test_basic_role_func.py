import click
import pytest

from epic_events.models.role import Role


def test_role_is_valid():
    valid_role = "support"
    result = Role().role_is_valid(None, valid_role)
    assert result == valid_role


def test_role_is_not_valid(capsys):
    invalid_role = "suport"
    with pytest.raises(click.UsageError):
        Role().role_is_valid(None, invalid_role)

    captured = capsys.readouterr()
    assert "\n'Invalid' role must be ==> 'support' or ' commercial' or 'management'.\n\n" in captured.out
