from epic_events.controllers.click_app import app
from epic_events.models.user import User
from epic_events.models.client import Client
from epic_events.models.contract import Contract
from epic_events.models.event import Event

from sqlalchemy import select
from unittest.mock import patch


def test_classic_managerial_path(runner, mocked_session):
    manager = mocked_session.scalar(
        select(User).where(User.name == 'Gabrielle Mallet'))

    with (patch('epic_events.controllers.click_app.create_database', return_value=mocked_session)):
        with patch(
                "epic_events.controllers.authenticate_controller.User.confirm_pass",
                return_value=True):
            result = runner.invoke(app, ['authenticate', 'login', '-e', manager.email], obj={"session": mocked_session})

            assert result.exit_code == 0
            assert "\n Welcome 'Gabrielle Mallet' you're logged.\n\n" in result.output

            # Check user list:

            result = runner.invoke(app, ['user', 'list-user'],
                                   obj={
                                       "session": mocked_session,
                                       "user_id": manager
                                   })

            # Find commercial he wanted
            assert '│ 6  │ Jules Evrard       │ evrard.jules-comm… │  ID : 3 - type :   │ ****' in result.output
            assert result.exit_code == 0

            # check clients list
            result = runner.invoke(app, ['client', 'list-client'],
                                   obj={
                                       "session": mocked_session,
                                       "user_id": manager
                                   })

            # Find client he want
            assert "│ 2  │   Noël   │ masson.… │   +33   │ Bouvet-… │ 24-10-… │ 10-11-2… │   ❌ " in result.output
            assert result.exit_code == 0

            # Modify Client  Noël to put Jules as commercial
            client_modified = mocked_session.scalar(select(Client).where(Client.id == 2))

            result = runner.invoke(app, ['client', 'modify-client', "-i", "2", "-ci", "6"],
                                   obj={
                                       "session": mocked_session,
                                       "user_id": manager
                                   })
            assert client_modified.commercial_contact_id is not None
            assert client_modified.commercial_contact_id == 6
            assert "\n 'NOËL MASSON' successfully modified.\n\n" in result.output
            assert result.exit_code == 0

            # check contracts list
            result = runner.invoke(app, ['contract', 'list-contract'],
                                   obj={
                                       "session": mocked_session,
                                       "user_id": manager
                                   })

            # Get the id of Noël Contract
            assert "│ 2  │ 374e557… │    2     │    3     │   1051   │  3671   │ 2023-11… │   ❌ " in result.output
            assert result.exit_code == 0

            # Modify Noël Contract as signed:
            contract = mocked_session.scalar(select(Contract).where(Contract.id == 2))

            result = runner.invoke(app,
                                   ["contract", "modify-contract", "-i", "2", "-s", "true"],
                                   obj={
                                       "session": mocked_session,
                                       "user_id": manager
                                   })

            assert contract.status is True
            assert result.exit_code == 0

            # Check Events list whitout support yet:
            result = runner.invoke(app, ['event', 'list-event', '-ns'],
                                   obj={
                                       "session": mocked_session,
                                       "user_id": manager
                                   })
            # Event N°2 as no support
            assert '│ 2  │ Noël-… │   2    │  None  │ 12-01… │ 13-01-… │ avenue │   204   │' in result.output
            # Event N°3 with support is not in résult.output
            assert '│ 3  │ Adrie… │   1    │   4    │ 24-12… │ 02-12-… │  62,   │   117   │  Main ' \
                   not in result.output
            event_choose = mocked_session.scalar(select(Event).where(Event.id == 2))
            assert event_choose.support_contact_id is None
            assert result.exit_code == 1

            # Manager assign support to Event N°2
            result = runner.invoke(app, ["event", "modify-event", "-i", "2", "-su", "4"],
                                   obj={
                                       "session": mocked_session,
                                       "user_id": manager
                                   })

            assert event_choose.support_contact_id is not None
            assert "\n Event 'Noël-Event' successfully modified.\n\n" in result.output
            assert result.exit_code == 0

            # logout
            result = runner.invoke(app, ['authenticate', 'logout'], obj={
                "session": mocked_session,
                "user_id": manager
            })

            assert result.exit_code == 0
            assert "\n' You have been successfully logout out'\n" in result.output
