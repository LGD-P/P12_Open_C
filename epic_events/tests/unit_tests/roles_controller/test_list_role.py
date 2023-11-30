from sqlalchemy import select

from epic_events.controllers.roles_controller import list_role
from epic_events.models.user import User


def test_list_all_roles(runner, mocked_session):
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


def test_list_single_role(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_role, ["-i", "1"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "│ 1  │  SUPPORT  │  User ID : 1 - Name : Kevin                  │" in result.output
    assert "│    │           │  User ID : 4 - Name : Alex-Élise Charpentier │" in result.output
    assert result.exit_code == 0


def test_list_role_without_authentication(runner, mocked_session):
    result = runner.invoke(list_role, ["-i", "1"],
                           obj={
                               "session": mocked_session,
                           })
    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
    assert result.exit_code == 1


def test_list_all_roles_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))
    result = runner.invoke(list_role,
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0
