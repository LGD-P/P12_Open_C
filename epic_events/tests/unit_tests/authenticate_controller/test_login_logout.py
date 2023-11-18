from epic_events.models.user import User
from epic_events.controllers.authenticate_controller import login, logout

from sqlalchemy import select
from unittest.mock import patch


def test_login(runner, mocked_session):
    user_to_log = mocked_session.scalar(
        select(User).where(User.name == "Denis Chamart"))

    with patch(
            "epic_events.controllers.authenticate_controller.User.confirm_pass",
            return_value=True):
        result = runner.invoke(login, ['-n', user_to_log.name],
                               obj={
                                   "session": mocked_session,
        })

    assert result.exit_code == 0
    assert "\n Welcome 'Denis Chamart' you're logged.\n\n" in result.output


def test_login_with_wrong_user(runner, mocked_session):
    with patch(
            "epic_events.controllers.authenticate_controller.User.confirm_pass",
            return_value=True):
        result = runner.invoke(login, ['-n', "Denis Chamar"],
                               obj={
                                   "session": mocked_session,
        })
    assert result.exit_code == 2
    assert "\n User with name 'Denis Chamar' is 'not found'.\n" in result.output


def test_login_with_wrong_password(runner, mocked_session):
    user_to_log = mocked_session.scalar(
        select(User).where(User.name == "Denis Chamart"))

    with patch(
            "epic_events.controllers.authenticate_controller.User.confirm_pass",
            return_value=False):
        result = runner.invoke(login, ['-n', user_to_log.name],
                               obj={
                                   "session": mocked_session,
        })

    assert result.exit_code == 2
    assert "\n' You enter a wrong password' \n" in result.output


def test_logout(runner, mocked_session):
    user_logged = mocked_session.scalar(
        select(User).where(User.name == "Denis Chamart"))

    result = runner.invoke(logout, obj={
        "session": mocked_session,
        "user_id": user_logged
    })

    assert "\n' You have been successfully logout out'\n" in result.output
