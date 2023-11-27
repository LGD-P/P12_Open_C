from epic_events.models.user import User
from epic_events.controllers.clients_controller import delete_client

from sqlalchemy import select


def test_delete_client(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(delete_client, ["-i", "1"], obj={
        "session": mocked_session,
        "user_id": user_logged
    })

    assert result.exit_code == 0
    assert "\n Client with ID '1', 'ADRIEN LELIÈVRE DE COSTE' has been 'deleted'.\n" in result.output


def test_delete_client_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))
    result = runner.invoke(delete_client, ["-i", "3"], obj={
        "session": mocked_session,
        "user_id": user_logged
    })

    assert result.exit_code == 0
    assert "\n' You're not allowed to use this command'\n\n" in result.output


def test_delete_client_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(delete_client, ["-i", "30"], obj={
        "session": mocked_session,
        "user_id": user_logged
    })

    assert result.exit_code == 0
    assert "\n Client with ID '30' is 'not found'.\n\n" in result.output


def test_delete_client_without_authentication(runner, mocked_session):
    result = runner.invoke(delete_client, ["-i", "30"], obj={
        "session": mocked_session,

    })

    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
    assert result.exit_code == 0
