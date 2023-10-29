from epic_events.models.client import Client
from epic_events.views.clients_views import (clients_table, created_succes, deleted_success,
                                             client_not_found, modification_done)

from datetime import datetime
import click
from sqlalchemy import select


@click.group()
@click.pass_context
def client(ctx):
    pass


@client.command()
@click.option('--id', '-i', help='Name of the table to query', required=False)
@click.pass_context
def list(ctx, id):
    session = ctx.obj['session']
    if id:
        client = session.scalar(select(Client).where(Client.id == id))
        if client is None:
            client_not_found(id)
        else:
            clients_table([client])
    else:
        clients_list = session.scalars(
            select(Client).order_by(Client.id)).all()

        clients_table(clients_list)


@client.command()
@click.option('--name', '-n', help='Full name for the new object', required=True)
@click.option('--email', '-e', help='Email for the new object', required=True)
@click.option('--phone', '-ph', help='Phone nummber', required=True)
@click.option('--company', '-c', help='Company name')
@click.pass_context
def create(ctx, name, email, phone, company):
    session = ctx.obj['session']

    creation = datetime.now()
    last_contact = datetime.now()
    company_name = None if company is None else company

    new_client = Client(full_name=name, email=email,
                        phone=phone, company_name=company_name,
                        creation_date=str(creation), last_contact_date=str(last_contact)
                        )
    session.add(new_client)
    session.commit()
    created_succes(new_client)


@client.command()
@click.option('--id', '-i', help='Id of the user you want to modify', required=True)
@click.option('--name', '-n', help='Full name for the new object')
@click.option('--email', '-e', help='Email for the new object')
@click.option('--phone', '-ph', help='Phone nummber')
@click.option('--company', '-c', help='Company name')
@click.pass_context
def modify(ctx, id, name, email, phone, company):
    session = ctx.obj['session']

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

        session.commit()
        modification_done(client_to_modify)
    else:
        client_not_found(id)


@client.command()
@click.option('--id', '-i', help='Id of the client you want to delete', required=True)
@click.pass_context
def delete(ctx, id):
    session = ctx.obj['session']

    client_to_delete = session.scalar(select(Client).where(Client.id == id))

    if client_to_delete:
        session.delete(client_to_delete)
        session.commit()
        deleted_success(id, client_to_delete)

    else:
        client_not_found(id)
