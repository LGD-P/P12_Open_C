from epic_events.models.user import User
from epic_events.controllers.clients_controller import list_client

from sqlalchemy import select


# Récupérer les ASSERT OUTPUT
def test_list_all_clients(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_client,
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 0


def test_list_single_client(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_client, ["-i", "1"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 0


def test_list_single_client_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_client, ["-i", "12"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert result.exit_code == 1
    assert "\n Client with ID '12' is 'not found'.\n" in result.output


def test_list_client_without_authentication(runner, mocked_session):
    result = runner.invoke(list_client, ["-i", "1"],
                           obj={"session": mocked_session})
    assert "\n' Invalid Token  please logged in again' \n" in result.output
    assert result.exit_code == 1
