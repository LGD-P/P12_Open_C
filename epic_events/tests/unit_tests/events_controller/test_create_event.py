from sqlalchemy import select
from epic_events.models.user import User
from epic_events.models.event import Event
from epic_events.controllers.events_controller import create


def test_create_event(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(create, [
        "-n", "John-Event", "-c", "2", "-su", "1", "-sd", "2024-01-01 - 19:00",
        "-ed", "2024-01-02 - 14:00", "-l", "Paris", "-a", "200", "-nt",
        "Epic Birthday"
    ],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    new_event = mocked_session.scalar(select(Event).where(Event.id == 4))
    assert new_event is not None
    assert result.exit_code == 0
    assert "\n ID N° 'N°4' Event 'John-Event'created successfully.\n\n" in result.output


def test_create_event_argument_missing(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(create, [
        "-n", "John-Event", "-c", "2", "-su", "-sd", "2024-01-01 - 19:00",
        "-ed", "2024-01-02 - 14:00", "-l", "Paris", "-a", "200", "-nt",
        "Epic Birthday"
    ],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })
    assert result.exit_code == 2
    assert "Missing option '--starting' / '-sd'." in result.output


def test_create_event_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))
    result = runner.invoke(create, [
        "-n", "John-Event", "-c", "2", "-su", "1", "-sd", "2024-01-01 - 19:00",
        "-ed", "2024-01-02 - 14:00", "-l", "Paris", "-a", "200", "-nt",
        "Epic Birthday"
    ],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0


# Modifier le controller try except
def test_create_event_without_authentication(runner, mocked_session):
    result = runner.invoke(create, [
        "-n", "John-Event", "-c", "2", "-su", "1", "-sd", "2024-01-01 - 19:00",
        "-ed", "2024-01-02 - 14:00", "-l", "Paris", "-a", "200", "-nt",
        "Epic Birthday"
    ],
                           obj={
                               "session": mocked_session,
                           })

    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
    assert result.exit_code == 0
