from datetime import datetime
from sqlalchemy import select
from epic_events.models.user import User
from epic_events.models.event import Event
from epic_events.controllers.events_controller import modify_event


def test_modify_event_name(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    event = mocked_session.scalar(select(Event).where(Event.id == 1))
    name_to_change = event.name
    result = runner.invoke(modify_event, ["-i", "1", "-n", "Maryse-Event"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert name_to_change != event.name
    assert "\n Event 'Maryse-Event' successfully modified.\n\n" in result.output
    assert result.exit_code == 0


def test_modify_wrong_support_team(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 4))
    result = runner.invoke(modify_event, ["-i", "1", "-n", "Maryse-Event"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n You are not in charge of the Event with ID '1' 'contact support team in charge "
    "to apply modifications'.\n\n" in result.output
    assert result.exit_code == 1


def test_modify_event_with_wrong_support(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(modify_event, ["-i", "1", "-su", "42"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n User with ID '42' is 'not found'.\n\n" in result.output
    assert result.exit_code == 1


def test_modify_event_with_wrong_contract(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(modify_event, ["-i", "1", "-c", "50"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n Contract with ID '50' is 'not found'.\n\n" in result.output
    assert result.exit_code == 1


def test_modify_event_support(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    event = mocked_session.scalar(select(Event).where(Event.id == 1))
    support_to_change = event.support_contact_id
    result = runner.invoke(modify_event, ["-i", "1", "-su", "4"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert event.support_contact_id != support_to_change
    assert "\n Event 'Alix-Event' successfully modified.\n\n" in result.output
    assert result.exit_code == 0


def test_modify_event_start_date(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    event = mocked_session.scalar(select(Event).where(Event.id == 1))
    start_date_to_change = event.start_date
    new_date = datetime(2024, 10, 10, 15)
    new_date_str = new_date.strftime("%Y-%m-%d - %H:%M")

    result = runner.invoke(modify_event, ["-i", "1", "-sd", new_date_str],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert event.start_date != start_date_to_change
    assert "\n Event 'Alix-Event' successfully modified.\n\n" in result.output
    assert result.exit_code == 0


def test_modify_event_start_date_with_wrong_format_args(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    new_date = datetime(2024, 10, 10, 15)
    new_date_str = new_date.strftime("%Y-%m-%d %H:%M")

    result = runner.invoke(modify_event, ["-i", "1", "-sd", new_date_str],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "'Date', must be written like this ==> 'YYYY-MM-DD - HH:MM '" in result.output
    assert result.exit_code == 0


def test_modify_event_end_date(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    event = mocked_session.scalar(select(Event).where(Event.id == 1))
    end_date_to_change = event.start_date
    new_date = datetime(2024, 10, 11, 15)
    new_date_str = new_date.strftime("%Y-%m-%d - %H:%M")

    result = runner.invoke(modify_event, ["-i", "1", "-sd", new_date_str],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert event.start_date != end_date_to_change
    assert "\n Event 'Alix-Event' successfully modified.\n\n" in result.output
    assert result.exit_code == 0


def test_modify_event_end_date_wrong_format_args(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    new_date = datetime(2024, 10, 11, 15)
    new_date_str = new_date.strftime("%Y/%m/%d - %H:%M")

    result = runner.invoke(modify_event, ["-i", "1", "-sd", new_date_str],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "'Date', must be written like this ==> 'YYYY-MM-DD - HH:MM '" in result.output
    assert result.exit_code == 0


def test_modify_event_location(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    event = mocked_session.scalar(select(Event).where(Event.id == 1))
    old_location = event.location

    result = runner.invoke(modify_event, ["-i", "1", "-l", "Nantes"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert event.location != old_location
    assert "\n Event 'Alix-Event' successfully modified.\n\n" in result.output
    assert result.exit_code == 0


def test_modify_event_attendees(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    event = mocked_session.scalar(select(Event).where(Event.id == 1))
    old_attendees = event.attendees

    result = runner.invoke(modify_event, ["-i", "1", "-a", "358"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert event.attendees != old_attendees
    assert "\n Event 'Alix-Event' successfully modified.\n\n" in result.output
    assert result.exit_code == 0


def test_modify_event_without_authentication(runner, mocked_session):
    result = runner.invoke(modify_event, ["-i", "1", "-n", "Maryse-Event"],
                           obj={
                               "session": mocked_session,
                           })
    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
    assert result.exit_code == 0
