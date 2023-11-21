from sqlalchemy import select
from unittest.mock import patch
from epic_events.controllers.user_controller import modify_user
from epic_events.models.user import User
import passlib.hash


def test_modify_user_name(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(modify_user, ["-i", "1", "-n", "Kevin Marley"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    assert "\n 'KEVIN MARLEY' successfully modified.\n\n" in result.output
    assert result.exit_code == 0

    user_modifyed = mocked_session.scalar(select(User).where(User.id == 1))
    assert user_modifyed.name == "Kevin Marley"


def test_modify_user_email(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(modify_user,
                           ["-i", "1", "-e", "Kevin.Marley@epicevents.com"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    assert "\n 'KEVIN' successfully modified.\n\n" in result.output
    assert result.exit_code == 0

    user_modifyed = mocked_session.scalar(select(User).where(User.id == 1))
    assert user_modifyed.email == "Kevin.Marley@epicevents.com"


def test_modify_user_role(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(modify_user, ["-i", "1", "-r", "management"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    assert "\n 'KEVIN' successfully modified.\n\n" in result.output
    assert result.exit_code == 0

    user_modifyed = mocked_session.scalar(select(User).where(User.id == 1))
    assert user_modifyed.role_id == 2


def test_modify_user_password(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    user_to_modify = mocked_session.scalar(select(User).where(User.id == 1))

    checking = passlib.hash.argon2.verify("S3CRET@23", user_to_modify.password)

    assert checking is True

    hash_new_password = passlib.hash.argon2.using(rounds=12).hash("NEW_PASS")

    with patch("epic_events.controllers.user_controller.change_password",
               return_value=hash_new_password):
        result = runner.invoke(modify_user, ["-i", "1", "-P"],
                               obj={
                                   "session": mocked_session,
                                   "user_id": user_logged
                               })

    user_modified = mocked_session.scalar(select(User).where(User.id == 1))

    checking = passlib.hash.argon2.verify("NEW_PASS", user_modified.password)

    assert checking is True

    assert "\n 'KEVIN' successfully modified.\n\n" in result.output
    assert result.exit_code == 0


def test_modify_user_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(modify_user, ["-i", "12", "-n", "Jacques André"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert f"\n User with ID '12' is 'not found'.\n" in result.output


def test_modify_user_name_without_authentication(runner, mocked_session):
    result = runner.invoke(modify_user, ["-i", "1", "-n", "Kevin Marley"],
                           obj={
                               "session": mocked_session,
                           })

    assert result.exit_code == 0
    assert "\n' Invalid Token  please logged in again' \n\n" in result.output


def test_modify_user_name_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))

    result = runner.invoke(modify_user, ["-i", "1", "-n", "Kevin Marley"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0
