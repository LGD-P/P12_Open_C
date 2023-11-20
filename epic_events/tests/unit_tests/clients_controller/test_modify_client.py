from epic_events.models.user import User
from epic_events.models.client import Client
from epic_events.controllers.clients_controller import modify

from sqlalchemy import select


def test_modify_client_full_name(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(modify, ["-i", "1", "-n", "Adrien Lelièvre"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    client_modified = mocked_session.scalar(select(Client).where(Client.id == 1))
    assert client_modified.full_name == "Adrien Lelièvre"
    assert result.exit_code == 0
    assert "\n 'ADRIEN LELIÈVRE' successfully modified.\n\n" in result.output


def test_modify_client_email(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(modify,
                           ["-i", "1", "-e", "Adrien.lelièvre@epicevents.com"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    client_modified = mocked_session.scalar(select(Client).where(Client.id == 1))
    assert client_modified.email != "lelièvre.adrien-client@epicevent.com"
    assert client_modified.email == "Adrien.lelièvre@epicevents.com"
    assert result.exit_code == 0
    assert "\n 'ADRIEN LELIÈVRE DE COSTE' successfully modified.\n\n" in result.output


def test_modify_client_phone(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(modify, ["-i", "1", "-ph", "+33 7 58 41 00 50"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    client_modified = mocked_session.scalar(select(Client).where(Client.id == 1))
    assert client_modified.phone != "+33 6 98 31 70 48"
    assert client_modified.phone == "+33 7 58 41 00 50"
    assert result.exit_code == 0
    assert "\n 'ADRIEN LELIÈVRE DE COSTE' successfully modified.\n\n" in result.output


def test_not_allowed_to_modify_client(runner, mocked_session):
    user_logged_as_support = mocked_session.scalar(
        select(User).where(User.id == 1))
    result = runner.invoke(modify, ["-i", "1", "-ph", "+33 7 58 41 00 50"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged_as_support
                           })

    assert result.exit_code == 0
    assert "\n' You're not allowed to use this command'\n\n" in result.output


def test_modify_client_without_authentication(runner, mocked_session):
    result = runner.invoke(modify, ["-i", "1", "-ph", "+33 7 58 41 00 50"],
                           obj={
                               "session": mocked_session,
                           })

    assert result.exit_code == 0
    assert "\n' Invalid Token  please logged in again' \n\n" in result.output


def test_modify_client_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(modify, ["-i", "12", "-ph", "+33 7 58 41 00 50"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 0
    assert "\n Client with ID '12' is 'not found'.\n\n" in result.output


def test_modify_client_missing_argument(
        runner,
        mocked_session,
):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(modify, ["-i", "1", "-ph"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 2
    assert "Error: Option '-ph' requires an argument.\n" in result.output
