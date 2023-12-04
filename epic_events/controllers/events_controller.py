from epic_events.utils import find_user_type, find_client_or_contract, \
    raise_invalid_token_if_user_not_logged_in_session
from epic_events.models.user import User
from epic_events.models.event import Event
from epic_events.models.contract import Contract
from epic_events.utils import has_permission
from epic_events.views.users_view import logged_as, invalid_token
from epic_events.views.events_views import (end_date_error, events_table,
                                            created_succes, deleted_success,
                                            event_not_found, modification_done,
                                            date_param, not_in_charge_of_this_event)
from epic_events.views.contracts_views import contract_not_signed

from datetime import datetime
import rich_click as click
from sqlalchemy import select
import sentry_sdk


@click.group()
@click.pass_context
def event(ctx):
    """Allows all users, within the limits of their permissions, to access various operations of the Events CRUD."""
    pass


@event.command()
@click.option('--id', '-i', help='Id of the event to query')
@click.option('--no-support', '-ns', is_flag=True, help='Only event without support')
@click.option('--team-support', '-ts', is_flag=True, help="Only event that you're in charge")
@click.pass_context
@has_permission(['management', 'support', 'commercial'])
def list_event(ctx, id, no_support, team_support):
    """List Event : no flag + all, -i + 'id' + 'id-event', -ns = no support team yet, ts = only you as team support
    are in charge"""
    session = ctx.obj['session']

    user_logged = raise_invalid_token_if_user_not_logged_in_session(ctx)

    if id:
        event = session.scalar(select(Event).where(Event.id == id))
        if event is None:
            raise click.UsageError(event_not_found(id))
        else:
            events_table([event])
    if no_support:
        event = session.scalars(select(Event).where(
            Event.support_contact_id.is_(None))).all()
        raise click.UsageError(events_table(event))

    if team_support:
        event = session.scalars(select(Event).where(
            Event.support_contact_id == user_logged.id)).all()
        return events_table(event)

    else:
        event_list = session.scalars(
            select(Event).order_by(Event.id)).all()

        events_table(event_list)
        logged_as(user_logged.name, user_logged.role.name)


@event.command()
@click.option('--name', '-n', help='Event name', required=True)
@click.option('--contract', '-c', help='Contract ID', required=True)
@click.option('--support', '-su', help='Support ID', required=True)
@click.option('--starting', '-sd',
              help='Starting date : format YYYY-MM-DD - HH:MM', required=True)
@click.option('--ending', '-ed',
              help='Ending date : format YYYY-MM-DD - HH:MM', required=True)
@click.option('--location', '-l', help='Location', required=True)
@click.option('--attendees', '-a', help='Attendees', required=True)
@click.option('--notes', '-nt', help='Notes')
@click.pass_context
@has_permission(['commercial'])
def create_event(ctx, name, contract, support, starting, ending, location, attendees,
                 notes):
    """Create Event : -n + 'name', -c + 'contract-ID', -su + 'Support-ID', -sd + 'startind-date', -ed + 'ending-date'
    -l + 'location', -a + 'attendees', -nt + 'notes' | date format is:  YYYY-MM-DD - HH:MM"""
    session = ctx.obj['session']

    user_logged = raise_invalid_token_if_user_not_logged_in_session(ctx)

    try:
        starting = datetime.strptime(starting, '%Y-%m-%d - %H:%M')
    except ValueError:
        sentry_sdk.capture_exception(date_param())

    try:
        ending = datetime.strptime(ending, '%Y-%m-%d - %H:%M')
    except ValueError:
        sentry_sdk.capture_exception(date_param())

    try:
        ending < starting
    except ValueError:
        sentry_sdk.capture_exception(end_date_error())

    contract_found = find_client_or_contract(ctx, Contract, contract)
    contract = session.scalar(
        select(Contract).where(Contract.id == contract_found))
    if contract.status is not True:
        raise click.UsageError(contract_not_signed(contract.id))

    support_found = find_user_type(ctx, support, 'support')

    new_event = Event(name=name, contract_id=contract_found,
                      support_contact_id=support_found, start_date=starting,
                      end_date=ending, location=location,
                      attendees=attendees, notes=notes)

    session.add(new_event)
    session.commit()
    created_succes(new_event)


@event.command()
@click.option('--id', '-i', help='Event ID', required=True)
@click.option('--name', '-n', help='Event name')
@click.option('--contract', '-c', help='Contract ID')
@click.option('--support', '-su', help='Support ID')
@click.option('--starting', '-sd',
              help='Starting date : format YYYY-MM-DD - HH:MM')
@click.option('--ending', '-e', help='Ending date : format YYYY-MM-DD - HH:MM')
@click.option('--location', '-l', help='Location')
@click.option('--attendees', '-a', help='Attendees')
@click.option('--notes', '-nt', help='Notes')
@click.pass_context
@has_permission(['management', 'support', 'commercial'])
def modify_event(ctx, id, name, contract, support, starting, ending,
                 location, attendees, notes):
    """Modify Event : -i + 'id', -n + 'event-name', -c + 'contract-id', -su + 'support-id' , -sd + 'starting-date'
    -e + 'ending-date', -l + 'location', - a + 'attentdees', -n + 'notes' | date format is:  YYYY-MM-DD - HH:MM"""
    session = ctx.obj['session']

    user_logged = raise_invalid_token_if_user_not_logged_in_session(ctx)

    event_to_modify = session.scalar(select(Event).where(Event.id == id))

    if event_to_modify:
        if user_logged.role.name == 'support':
            if event_to_modify.support_contact_id == user_logged.id:
                pass
            else:
                raise ValueError(
                    not_in_charge_of_this_event(event_to_modify.id))

        if name is not None:
            event_to_modify.name = name

        if contract is not None:
            contract_found = find_client_or_contract(ctx, Contract, contract)
            event_to_modify.contract_id = contract_found

        if support is not None:
            support_found = find_user_type(ctx, support, 'support')
            event_to_modify.support_contact_id = support_found

        if starting is not None:
            try:
                starting = datetime.strptime(starting, '%Y-%m-%d - %H:%M')
                event_to_modify.start_date = starting
            except ValueError:
                return date_param()

        if ending is not None:
            try:
                ending = datetime.strptime(ending, '%Y-%m-%d - %H:%M')
                event_to_modify.end_date = ending
            except ValueError:
                return date_param()

        if location is not None:
            event_to_modify.location = location

        if attendees is not None:
            event_to_modify.attendees = attendees

        if notes is not None:
            event_to_modify.notes = notes

        session.commit()
        modification_done(event_to_modify)
    else:
        raise click.UsageError(event_not_found(id))


@event.command()
@click.option('--id', '-i', help='Id of the event you want to delete',
              required=True)
@click.pass_context
@has_permission(['management', 'support', 'commercial'])
def delete_event(ctx, id):
    """Delete Event : -i + 'id' of the event you want to delete"""
    session = ctx.obj['session']

    raise_invalid_token_if_user_not_logged_in_session(ctx)

    event_to_delete = session.scalar(select(Event).where(Event.id == id))

    if event_to_delete:
        session.delete(event_to_delete)
        session.commit()
        deleted_success(id, event_to_delete)

    else:
        raise click.UsageError(event_not_found(id))