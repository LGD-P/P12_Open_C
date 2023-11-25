from epic_events.models.user import User
from epic_events.models.client import Client
from epic_events.controllers.clients_controller import create_client

from sqlalchemy import select



def test_create_client(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))

    result = runner.invoke(create_client, [
        "-n", 'Georges Piotr', "-e", "geogres-piotr@gpsas.com", "-ph",
        "+33 6 98 31 70 48", "-c", "GP-SAS & Co.", "-ci","3"
    ],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    user_created = mocked_session.scalar(
        select(Client).where(Client.full_name == "Georges Piotr"))


    assert user_created.full_name == "Georges Piotr"
    assert "\n 'GEORGES PIOTR' created successfully.\n" in result.output
    assert result.exit_code == 0


def test_create_client_with_missing_argument(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))

    result = runner.invoke(create_client, [
        "-n", "-e", "geogres-piotr@gpsas.com", "-ph", "+33 6 98 31 70 48", "-c",
        "GP-SAS & Co."
    ],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 2
    assert "Missing option '--email' / '-e" in result.output


def test_create_client_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))

    result = runner.invoke(create_client, [
        "-n", 'Georges Piotr', "-e", "geogres-piotr@gpsas.com", "-ph",
        "+33 6 98 31 70 48", "-c", "GP-SAS & Co."
    ],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0


def test_create_client_without_authentication(runner, mocked_session):
    result = runner.invoke(create_client, [
        "-n", 'Georges Piotr', "-e", "geogres-piotr@gpsas.com", "-ph",
        "+33 6 98 31 70 48", "-c", "GP-SAS & Co."
    ],
                           obj={
                               "session": mocked_session,
                           })

    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
    assert result.exit_code == 0
