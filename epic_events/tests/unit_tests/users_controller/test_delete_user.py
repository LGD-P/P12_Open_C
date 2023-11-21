from sqlalchemy import select
from sqlalchemy.orm import session

from epic_events.controllers.user_controller import delete_user
from epic_events.models.user import User


def test_delete_user(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(delete_user, ["-i", "3"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n User with ID '3', 'PIERRE' has been 'deleted'.\n\n" in result.output
    assert result.exit_code == 0


def test_delete_user_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(delete_user, ["-i", "9"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n User with ID '9' is 'not found'.\n\n" in result.output
    assert result.exit_code == 0


def test_delete_user_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))

    result = runner.invoke(delete_user, ["-i", "2"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0


def test_delete_user_without_authentication(runner, mocked_session):
    result = runner.invoke(delete_user, ["-i", "3"],
                           obj={
                               "session": mocked_session,
                           })

    assert result.exit_code == 0
    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
