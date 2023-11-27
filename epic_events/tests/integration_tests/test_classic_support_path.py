from epic_events.controllers.click_app import app
from epic_events.models.user import User
from epic_events.models.event import Event

from sqlalchemy import select
from unittest.mock import patch


def test_classic_support_path(runner, mocked_session):
    support = mocked_session.scalar(
        select(User).where(User.name == 'Alex-Élise Charpentier'))

    with patch('epic_events.controllers.click_app.create_database', return_value=mocked_session):
        with patch(
                "epic_events.controllers.authenticate_controller.User.confirm_pass",
                return_value=True):
            result = runner.invoke(app, ['authenticate', 'login', '-n', support.name],
                                   obj={"session": mocked_session})

            assert result.exit_code == 0
            assert "\n Welcome 'Alex-Élise Charpentier' you're logged.\n\n" in result.output

            # list event that Alex-Elise is in change:

            result = runner.invoke(app, ['event', 'list-event', '-ts'],
                                   obj={
                                       "session": mocked_session,
                                       "user_id": support
                                   })

            assert '┃ ID ┃  Name  ┃ Contr… ┃ Suppo… ┃ Start… ┃ End da… ┃ Locat… ┃ Attend… ┃ Notes  ┃' in result.output
            assert '│ 3  │ Adrie… │   1    │   4    │ 24-12… │ 02-12-… │  62,   │   117   │  Main  │' in result.output
            assert result.exit_code == 0

            # Modify attendees of this event :

            event = mocked_session.scalar(select(Event).where(Event.id == '3'))
            old_attendees = event.attendees

            result = runner.invoke(app, ['event', 'modify-event', "-i", "3", "-a", "130"],
                                   obj={
                                       "session": mocked_session,
                                       "user_id": support
                                   })

            assert event.attendees != old_attendees
            assert "\n Event 'Adrien-Event' successfully modified.\n\n" in result.output
            assert result.exit_code == 0

        # logout
        result = runner.invoke(app, ['authenticate', 'logout'], obj={
            "session": mocked_session,
            "user_id": support
        })

        assert result.exit_code == 0
        assert "\n' You have been successfully logout out'\n" in result.output
