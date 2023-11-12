import click

from epic_events.models.role import Role
from epic_events.views.users_view import invalid_role

def test_role_is_valid():
    valid_roles = ["support", "commercial", "management"]
    for role in valid_roles:
        result = Role().role_is_valid(None, role)
        assert result == role

def test_role_is_notvalid():
    role = "comercial"
    valid_roles = ["support", "commercial", "management"]
    for r in valid_roles:
        if role in r:
            result = Role().role_is_valid(None, role)
            assert invalid_role()
            assert result == click.UsageError("Invalid role")

