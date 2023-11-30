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
        result = runner.invoke(login, ['-e', user_to_log.email],
                               obj={
                                   "session": mocked_session,
                               })

    assert result.exit_code == 0
    assert "\n Welcome 'Denis Chamart' you're logged.\n\n" in result.output


def test_login_with_wrong_user(runner, mocked_session):
    with patch(
            "epic_events.controllers.authenticate_controller.User.confirm_pass",
            return_value=True):
        result = runner.invoke(login, ['-e', "Denis Chamartt@epic.com"],
                               obj={
                                   "session": mocked_session,
                               })

    assert result.exit_code == 0
    assert "\n User with email 'Denis Chamartt@epic.com' is 'not found'.\n\n" in result.output


def test_login_with_wrong_password(runner, mocked_session):
    with patch(
            "epic_events.controllers.authenticate_controller.User.confirm_pass",
            return_value=False):
        result = runner.invoke(login, ['-e', "Denis Chamartt@epicevent.com"],
                               obj={
                                   "session": mocked_session,
                               })

    assert result.exit_code == 0
    assert "\n' You enter a wrong password' \n" in result.output


def test_logout(runner, mocked_session):
    user_logged = mocked_session.scalar(
        select(User).where(User.email == "Denis Chamartt@epicevent.com"))

    result = runner.invoke(logout, obj={
        "session": mocked_session,
        "user_id": user_logged
    })

    assert result.exit_code == 0
    assert "\n' You have been successfully logout out'\n" in result.output


def test_logout_without_being_logged(runner, mocked_session):
    result = runner.invoke(logout, obj={
        "session": mocked_session,

    })

    assert result.exit_code == 0
    assert "\n' Invalid Token  please logged in again' \n" in result.output
