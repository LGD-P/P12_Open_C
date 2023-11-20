from epic_events.models.user import User
from epic_events.models.event import Event
from epic_events.utils import has_permission
from epic_events.views.users_view import logged_as, invalid_token
from epic_events.views.events_views import (end_date_error, events_table,
                                            created_succes, deleted_success,
                                            event_not_found, modification_done,
                                            date_param)

from datetime import datetime
import click
from sqlalchemy import select


@click.group()
@click.pass_context
def event(ctx):
    pass


@event.command(name='list')
@click.option('--id', '-i', help='Id of the event to query')
@click.pass_context
@has_permission(['management', 'support', 'commercial'])
def list_event(ctx, id):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id)
        )
        if id:
            event = session.scalar(select(Event).where(Event.id == id))
            if event is None:
                event_not_found(id)
            else:
                events_table([event])
        else:
            event_list = session.scalars(
                select(Event).order_by(Event.id)).all()

            events_table(event_list)
            logged_as(user_logged.name, user_logged.role.name)

    except KeyError:
        invalid_token()


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
def create(ctx, name, contract, support, starting, ending, location, attendees,
           notes):
    session = ctx.obj['session']
    try:
      user_logged = session.scalar(
        select(User).where(User.id == ctx.obj['user_id'].id)
    )
    
  
      try:
          starting = datetime.strptime(starting, '%Y-%m-%d - %H:%M')
      except ValueError:
          return date_param()
  
      try:
          ending = datetime.strptime(ending, '%Y-%m-%d - %H:%M')
      except ValueError:
          return date_param()
  
      if ending < starting:
          return end_date_error()
  
      new_event = Event(name=name, contract_id=contract,
                        support_contact_id=support, start_date=starting,
                        end_date=ending, location=location,
                        attendees=attendees, notes=notes)
  
      session.add(new_event)
      session.commit()
      created_succes(new_event)

    except KeyError:
      invalid_token()


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
def modify(ctx, id, name, contract, support, starting, ending,
           location, attendees, notes):
    session = ctx.obj['session']
    try:
      user_logged = session.scalar(
      select(User).where(User.id == ctx.obj['user_id'].id)
  )

      event_to_modify = session.scalar(select(Event).where(Event.id == id))
  
      if event_to_modify:
  
          if name is not None:
              event_to_modify.name = name
            
          if contract is not None:
              event_to_modify.contact_id = contract
  
          if support is not None:
              event_to_modify.support_contact_id = support
  
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
          event_not_found(id)

    except KeyError:
      invalid_token()
  

@event.command()
@click.option('--id', '-i', help='Id of the event you want to delete',
              required=True)
@click.pass_context
@has_permission(['management', 'support', 'commercial'])
def delete(ctx, id):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
        select(User).where(User.id == ctx.obj['user_id'].id)
    )

        event_to_delete = session.scalar(select(Event).where(Event.id == id))
    
        if event_to_delete:
            session.delete(event_to_delete)
            session.commit()
            deleted_success(id, event_to_delete)
    
        else:
            event_not_found(id)
        
    except KeyError:
      invalid_token()
