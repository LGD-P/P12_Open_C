from epic_events.models.user import User
from epic_events.controllers.user_controller import create_user

from sqlalchemy import select


def test_create_user(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(create_user, [
        "-n",
        "Charles Henri",
        "-e",
        "Charles.Henri@epicevents.com",
        "-r",
        "support",
    ],
                           input="S3cret@2024",
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    assert result.exit_code == 0
    assert "\n 'CHARLES HENRI' created successfully.\n" in result.output

    new_user = mocked_session.scalar(
        select(User).where(User.name == "Charles Henri"))

    assert new_user.id == 7
    assert new_user.role_id == 1
    assert new_user.name == "Charles Henri"


def test_create_user_with_wrong_role(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(create_user, [
        "-n",
        "Charles Henri",
        "-e",
        "Charles.Henri@epicevents.com",
        "-r",
        "wrong",
    ],
                           input="S3cret@2024",
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "'Invalid' role must be ==> 'support' or ' commercial' or 'management'." in result.output


def test_create_user_with_wrong_email(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(create_user, [
        "-n",
        "Charles Henri",
        "-e",
        "Charles.Henriepicevents.com",
        "-r",
        "management",
    ],
                           input="S3cret@2024",
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\nThe 'Email' you provided is 'invalid'\n" in result.output


def test_create_user_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))

    result = runner.invoke(create_user, [
        "-n",
        "Charles Henri",
        "-e",
        "Charles.Henri@epicevents.com",
        "-r",
        "support",
    ],
                           input="S3cret@2024",
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    assert "\n\n' You're not allowed to use this command'\n\n" in result.output in result.output
    assert result.exit_code == 0


def test_create_without_authentication(runner, mocked_session):
    result = runner.invoke(create_user, [
        "-n",
        "Charles Henri",
        "-e",
        "Charles.Henri@epicevents.com",
        "-r",
        "support",
    ],
                           input="S3cret@2024",
                           obj={
                               "session": mocked_session,
                           })
    assert result.exit_code == 1
    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
