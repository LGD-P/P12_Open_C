from sqlalchemy import select

from epic_events.controllers.user_controller import list_user
from epic_events.models.user import User


def test_list_users(runner, mocked_session):
    """Test users list command"""

    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_user,
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 0
    assert "│ 1  │ Kevin              │ keven@epicevent.c… │  ID : 1 - type :   │ ****" in result.output
    assert "│ 2  │ Denis Chamart      │ Denis              │  ID : 2 - type :   │ ****" in result.output
    assert "│ 3  │ Pierre             │ Pierre@epicevent.… │  ID : 3 - type :   │ **** " in result.output


def test_list_user_not_allowed(runner, mocked_session):
    """Test list_user with a user not allowed """
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))
    result = runner.invoke(list_user,
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 0
    assert "\n' You're not allowed to use this command'\n" in result.output


def test_list_user_single(runner, mocked_session):
    """Test list_user when only one user is searched"""
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(list_user, ["--id", "1"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    print(result.output)
    assert result.exit_code == 0
    assert "│ 1  │ Kevin │ keven@epicevent.com │  ID : 1 - type : support │ ****     │" in result.output


def test_list_user_not_found(runner, mocked_session):
    """Test list_user with a wrong id"""
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(list_user, ["--id", "12"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 1
    assert "\n User with ID '12' is 'not found'.\n" in result.output


def test_list_user_invalid_token(runner, mocked_session):
    """Test list_user with  no user logged"""

    result = runner.invoke(list_user, ["--id", "2"],
                           obj={
                               "session": mocked_session,
                           })

    assert result.exit_code == 0
    assert "\n' Invalid Token  please logged in again' \n" in result.output
