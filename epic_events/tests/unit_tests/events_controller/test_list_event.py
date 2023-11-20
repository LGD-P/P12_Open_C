from sqlalchemy import select
from epic_events.models import user
from epic_events.models.user import User
from epic_events.models.event import Event
from epic_events.controllers.events_controller import list_event



def test_list_all_events(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(list_event,
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    print(result.output)
    assert '│ 1  │ Michè… │   3    │   1    │ 10-10… │ 11-10-… │  60,   │   476   │  Côte ' in result.output
    assert '│ 2  │ René-… │   3    │  None  │ 12-01… │ 13-01-… │ avenue │   204   │ Claire ' in result.output
    assert result.exit_code == 0


def test_list_single_event(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(list_event, ['-i', '3'],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert '│ 3  │ René-… │   3    │  None  │ 24-12… │ 02-12-… │  62,   │   117   │  Main ' in result.output
    assert result.exit_code == 0


def test_list_with_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(list_event, ['-i', '12'],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n Event with ID '12' is 'not found'.\n" in result.output
    assert result.exit_code == 0


def test_list_events_without_authentication(runner, mocked_session):
    result = runner.invoke(list_event,
                           obj={
                               "session": mocked_session,
                           })

    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
    assert result.exit_code == 0
