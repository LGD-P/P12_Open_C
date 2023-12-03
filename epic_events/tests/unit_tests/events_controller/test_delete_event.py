from sqlalchemy import select
from epic_events.models.user import User
from epic_events.models.event import Event
from epic_events.controllers.events_controller import delete_event


def test_delete_event(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    event_to_delete = mocked_session.scalar(select(Event).where(Event.id == 1))
    result = runner.invoke(delete_event, ["-i", "1"],
                           obj={"session": mocked_session,
                                'user_id': user_logged})

    assert f"Event with ID '{event_to_delete.id}', '{event_to_delete.name}' has been 'deleted'" in result.output
    assert result.exit_code == 0


def test_delete_event_with_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(delete_event, ["-i", "19"],
                           obj={"session": mocked_session,
                                'user_id': user_logged})

    assert "\n Event with ID '19' is 'not found'.\n\n" in result.output
    assert result.exit_code == 1


def test_delete_event_without_authentication(runner, mocked_session):
    result = runner.invoke(delete_event, ["-i", "1"],
                           obj={"session": mocked_session})

    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
    assert result.exit_code == 0
