from sqlalchemy import select

from epic_events.controllers.roles_controller import list_role
from epic_events.models.user import User


def test_list_roles(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_role,
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    assert result.exit_code == 0
    assert "MANAGEMENT" in result.output
    assert "SUPPORT" in result.output
    assert "COMMERCIAL" in result.output


def test_list_role_with_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_role, ["-i", "1"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "│ 1  │  SUPPORT  │  User ID : 1 - Name : Kevin │" in result.output
    assert result.exit_code == 0
