from epic_events.models.user import User
from epic_events.models.client import Client
from epic_events.controllers.clients_controller import modify_client

from sqlalchemy import select


def test_modify_client_full_name(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    client_modified = mocked_session.scalar(select(Client).where(Client.id == 1))
    old_client_name = client_modified.full_name

    result = runner.invoke(modify_client, ["-i", "1", "-n", "Adrien Lelièvre"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    client_modified = mocked_session.scalar(select(Client).where(Client.id == 1))
    assert client_modified.full_name == "Adrien Lelièvre"
    assert client_modified.full_name != old_client_name
    assert result.exit_code == 0
    assert "\n 'ADRIEN LELIÈVRE' successfully modified.\n\n" in result.output


def test_modify_client_email(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(modify_client,
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
    result = runner.invoke(modify_client, ["-i", "1", "-ph", "+33 7 58 41 00 50"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    client_modified = mocked_session.scalar(select(Client).where(Client.id == 1))
    assert client_modified.phone != "+33 6 98 31 70 48"
    assert client_modified.phone == "+33 7 58 41 00 50"
    assert result.exit_code == 0
    assert "\n 'ADRIEN LELIÈVRE DE COSTE' successfully modified.\n\n" in result.output


def test_modify_client_commercial_contrat_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    client_modified = mocked_session.scalar(select(Client).where(Client.id == 1))
    result = runner.invoke(modify_client,
                           ["-i", "1", "-ci", "6"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert client_modified.commercial_contact_id is not None
    assert client_modified.commercial_contact_id == 6
    assert "\n 'ADRIEN LELIÈVRE DE COSTE' successfully modified.\n\n" in result.output
    assert result.exit_code == 0


def test_not_allowed_to_modify_client(runner, mocked_session):
    user_logged_as_support = mocked_session.scalar(
        select(User).where(User.id == 1))
    result = runner.invoke(modify_client, ["-i", "1", "-ph", "+33 7 58 41 00 50"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged_as_support
                           })

    assert result.exit_code == 0
    assert "\n' You're not allowed to use this command'\n\n" in result.output


def test_commercial_not_allowed_to_modify_client_not_in_charge(runner, mocked_session):
    user_logged_as_support = mocked_session.scalar(
        select(User).where(User.id == 3))
    result = runner.invoke(modify_client, ["-i", "3", "-ph", "+33 7 58 41 00 50"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged_as_support
                           })

    assert result.exit_code == 1
    assert "\n' As commercial you are 'not in charge' of Client : ID '1'. You're 'not allowed' "
    "to modify this client.\n\n" in result.output


def test_modify_client_without_authentication(runner, mocked_session):
    result = runner.invoke(modify_client, ["-i", "1", "-ph", "+33 7 58 41 00 50"],
                           obj={
                               "session": mocked_session,
                           })

    assert result.exit_code == 0
    assert "\n' Invalid Token  please logged in again' \n\n" in result.output


def test_modify_client_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(modify_client, ["-i", "12", "-ph", "+33 7 58 41 00 50"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 1
    assert "\n Client with ID '12' is 'not found'.\n\n" in result.output


def test_modify_client_missing_argument(
        runner,
        mocked_session,
):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(modify_client, ["-i", "1", "-ph"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 2
    assert "Option '-ph' requires an argument." in result.output
