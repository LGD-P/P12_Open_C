from epic_events.controllers.click_app import app
from epic_events.models.user import User
from epic_events.models.client import Client

from sqlalchemy import select
from unittest.mock import patch


def test_classic_commercial_path(runner, mocked_session, mock_db):
    commercial = mocked_session.scalar(
        select(User).where(User.name == 'Jules Evrard'))

    with patch(
            "epic_events.controllers.authenticate_controller.User.confirm_pass",
            return_value=True):
        result = runner.invoke(
            app, ['authenticate', 'login', '-e', commercial.email])
        # mock_db.assert_called_once()
        assert result.exit_code == 0
        assert "\n Welcome 'Jules Evrard' you're logged.\n\n" in result.output

        # Create a new client :
        result = runner.invoke(app, ['client', 'create-client',
                                     '-n', 'Hugues Devaux', '-e', 'devaux.hugues-client@epicevent.com',
                                     '-ph', '+33 (0)5 86 47 21 65',
                                     '-c', 'Collin & Co.',
                                     '-ci', '6'],
                               obj={
                                   "user_id": commercial
        })

        assert "\n 'HUGUES DEVAUX' created successfully.\n\n" in result.output
        assert result.exit_code == 0

        # Modify client because error on phone number :
        result = runner.invoke(app, ['client', 'modify-client', "-i", "4", "-ph", "+33 7 58 41 00 50"],
                               obj={
                                   "user_id": commercial
                                   })

        client_modified = mocked_session.scalar(
            select(Client).where(Client.id == 4))

        assert client_modified.phone != "+33 (0)5 86 47 21 65"
        assert client_modified.phone == "+33 7 58 41 00 50"
        assert "\n 'HUGUES DEVAUX' successfully modified.\n\n" in result.output
        assert result.exit_code == 0

        # Try to Modify client that is not allowed to :
        result = runner.invoke(app, ['client', 'modify-client', "-i", "1", "-e", "Adrien.ldc@epicevents.com"],
                               obj={
                                   "user_id": commercial
                                   })

        assert "\n As commercial you are 'not in charge' of Client : ID '1'. You're 'not allowed' "
        "\nto modify this client.\n\n" in result.output
        assert result.exit_code == 1

        # logout
        result = runner.invoke(app, ['authenticate', 'logout'], obj={
            "user_id": commercial
            })

        assert result.exit_code == 0
        assert "\n' You have been successfully logout out'\n" in result.output
