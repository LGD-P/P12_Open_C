from models.models import Event, session
from views.events_views import (
    events_table, table_not_found, param_required, created_succes,
    deleted_success, event_not_found, modification_done)

from datetime import datetime
import psycopg2
import click


class EventApp():

    @click.group()
    @click.option('--host', '-h', default='localhost', help='Database host')
    @click.option('--port', '-p', default=5432, help='Database port')
    @click.option('--user', '-u', default='postgres', help='Database user')
    @click.option('--password', '-P', default='MyPassIs23Word', help='Database password')
    @click.option('--dbname', '-d', default='postgres', help='Database name')
    @click.pass_context
    def connect(ctx, host, port, user, password, dbname):
        ctx.ensure_object(dict)
        ctx.obj['conn'] = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to query', required=True)
    @click.pass_context
    def access_events(ctx, table):
        conn = ctx.obj['conn']

        if table == 'events':
            events = session.query(Event).all()
            events_table(events, table)
            session.close()
        else:
            table_not_found(table)

        conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to create in', required=True)
    @click.option('--name', '-n', help='Event name', required=True)
    @click.option('--contract', '-c', help='Contract ID', required=True)
    @click.option('--support', '-su', help='Support ID', required=True)
    @click.option('--starting', '-sd', help='Starting date : format YYYY-MM-DD - HH:MM', required=True)
    @click.option('--ending', '-e', help='Ending date : format YYYY-MM-DD - HH:MM', required=True)
    @click.option('--location', '-l', help='Location', required=True)
    @click.option('--attendees', '-a', help='Attendees', required=True)
    @click.option('--notes', '-nt', help='Notes')
    @click.pass_context
    def create_event(ctx, table, name, contract, support, starting, ending, location, attendees, notes):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'events':
            # a vérifier...
            if not name or not contract or not support or not starting or not ending or not location or not attendees:
                param_required()
            else:

                starting = datetime.strptime(starting, '%Y-%m-%d - %H:%M')
                ending = datetime.strptime(ending, '%Y-%m-%d - %H:%M')

                new_event = Event(name=name, contract_id=contract, support_contact_id=support,
                                  start_date=starting, end_date=ending, location=location,
                                  attendees=attendees, notes=notes)

                session.add(new_event)
                session.commit()
                created_succes(new_event)

            cur.close()
            conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to create in', required=True)
    @click.option('--id', '-i', help='Event ID', required=True)
    @click.option('--name', '-n', help='Event name')
    @click.option('--contract', '-c', help='Contract ID')
    @click.option('--support', '-su', help='Support ID')
    @click.option('--starting', '-sd', help='Starting date : format YYYY-MM-DD - HH:MM')
    @click.option('--ending', '-e', help='Ending date : format YYYY-MM-DD - HH:MM')
    @click.option('--location', '-l', help='Location')
    @click.option('--attendees', '-a', help='Attendees')
    @click.option('--notes', '-nt', help='Notes')
    @click.pass_context
    def modify_event(ctx, table, id, name, contract, support, starting, ending,
                     location, attendees, notes):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'events':
            event_to_modify = session.query(
                Event).filter_by(id=id).first()

            if event_to_modify:

                if name is not None:
                    event_to_modify.name = name
                if contract is not None:
                    event_to_modify.contact_id = contract

                if support is not None:
                    event_to_modify.support_contact_id = support

                if starting is not None:
                    event_to_modify.start_date = starting

                if ending is not None:
                    event_to_modify.end_date = ending

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
        else:
            table_not_found(table)

        cur.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to query', required=True)
    @click.option('--id', '-i', help='Id of the event you want to delete', required=True)
    @click.pass_context
    def delete_event(ctx, table, id):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'events':
            event_to_delete = session.query(Event).filter_by(id=id).first()

            if event_to_delete:
                session.delete(event_to_delete)
                session.commit()
                deleted_success(id, event_to_delete)

            else:
                event_not_found(id)
        else:
            table_not_found(table)
        cur.close()
        conn.close()
