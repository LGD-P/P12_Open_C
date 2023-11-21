from epic_events.models.user import User
from epic_events.models.client import Client
from epic_events.utils import has_permission
from epic_events.views.users_view import logged_as, invalid_token
from epic_events.views.clients_views import (clients_table, created_succes,
                                             deleted_success, client_not_found,
                                             modification_done, commercial_not_found
                                             )

from datetime import datetime
import click
from sqlalchemy import select


@click.group()
@click.pass_context
def client(ctx):
    pass


@client.command(name='list')
@click.option('--id', '-i', help='ID of client to query', required=False)
@click.pass_context
@has_permission(['management', 'support', 'commercial'])
def list_client(ctx, id):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        if id:
            client = session.scalar(select(Client).where(Client.id == id))
            if client is None:
                client_not_found(id)
            else:
                clients_table([client])
        else:
            clients_list = session.scalars(select(Client).order_by(Client.id)).all()

            clients_table(clients_list)
            logged_as(user_logged.name, user_logged.role.name)

    except KeyError:
        invalid_token()
        pass


@client.command()
@click.option('--name',
              '-n',
              help='Full name for the new object',
              required=True)
@click.option('--email', '-e', help='Email for the new object', required=True)
@click.option('--phone', '-ph', help='Phone number', required=True)
@click.option('--company', '-c', help='Company name')
@click.option('--comid', '-ci', help='Commercial id')
@click.pass_context
@has_permission(['commercial', 'management'])
def create(ctx, name, email, phone, company, comid):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        if comid is not None:
            user_list = session.scalars(select(User).order_by(User.id)).all()
            for element in user_list:
                if element.id == int(comid) and element.role.name == "commercial":
                    return comid
            return commercial_not_found(comid)

        creation = datetime.utcnow()
        last_contact = datetime.utcnow()
        company_name = None if company is None else company

        new_client = Client(full_name=name,
                            email=email,
                            phone=phone,
                            company_name=company_name,
                            creation_date=creation,
                            last_contact_date=last_contact,
                            commercial_contact_id=comid)

        session.add(new_client)
        session.commit()
        created_succes(new_client)

    except KeyError:
        invalid_token()
        pass


@client.command()
@click.option('--id',
              '-i',
              help='Id of the user you want to modify',
              required=True)
@click.option('--name', '-n', help='Full name for the new object')
@click.option('--email', '-e', help='Email for the new object')
@click.option('--phone', '-ph', help='Phone nummber')
@click.option('--company', '-c', help='Company name')
@click.option('--comid', '-ci', help='User id of your commercial')
@click.pass_context
@has_permission(['management', 'commercial'])
def modify(ctx, id, name, email, phone, company, comid):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        client_to_modify = session.scalar(select(Client).where(Client.id == id))

        if client_to_modify:

            if name is not None:
                client_to_modify.full_name = name
            if email is not None:
                client_to_modify.email = email

            if phone is not None:
                client_to_modify.phone = phone

            if company is not None:
                client_to_modify.company_name = company

            client_to_modify.last_contact_date = datetime.now()

            if comid is not None:
                commercial_found = False
                user_list = session.scalars(select(User).order_by(User.id)).all()
                for element in user_list:
                    if element.id == int(comid) and element.role.name == "commercial":
                        client_to_modify.commercial_contact_id = comid
                        commercial_found = True
                if not commercial_found:
                    return commercial_not_found(comid)

            session.commit()
            modification_done(client_to_modify)
        else:
            client_not_found(id)
    except KeyError:
        invalid_token()
        pass


@client.command()
@click.option('--id',
              '-i',
              help='Id of the client you want to delete',
              required=True)
@click.pass_context
@has_permission(['management', 'commercial'])
def delete(ctx, id):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        client_to_delete = session.scalar(select(Client).where(Client.id == id))

        if client_to_delete:
            session.delete(client_to_delete)
            session.commit()
            deleted_success(id, client_to_delete)

        else:
            client_not_found(id)

    except KeyError:
        invalid_token()
        pass
