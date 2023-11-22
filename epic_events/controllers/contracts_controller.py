import uuid
from epic_events.models.client import Client
from epic_events.models.user import User
from epic_events.models.contract import Contract
from epic_events.utils import has_permission
from epic_events.views.clients_views import client_not_found
from epic_events.views.users_view import logged_as, invalid_token, user_not_found
from epic_events.views.contracts_views import (contracts_table, created_succes,
                                               deleted_success,
                                               contract_not_found,
                                               modification_done)

import click

from sqlalchemy import select


@click.group()
@click.pass_context
def contract(ctx):
    """Allows the MANAGEMENT & COMMERCIAL, within the limits of their permissions,
     to access various operations of the Contracts CRUD ."""
    pass


@contract.command()
@click.option("--id", "-i", help="id of the event to search", )
@click.pass_context
@has_permission(['management', 'commercial'])
def list_contract(ctx, id):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))
        if id:
            contract = session.scalar(
                select(Contract).where(Contract.id == id))
            if contract is None:
                contract_not_found(id)
            else:
                contracts_table([contract])
        else:
            contract_list = session.scalars(
                select(Contract).order_by(Contract.id)).all()

            contracts_table(contract_list)
            logged_as(user_logged.name, user_logged.role.name)
    except KeyError:
        invalid_token()
        pass


@contract.command()
@click.option('--client', '-c', help='Client ID', required=True)
@click.option('--management', '-m', help='Management ID', required=True)
@click.option('--total', '-ta', help='Total Amount', required=True)
@click.option('--remain', '-r', help='Remaining Amount', required=True)
@click.option('--status', '-s', help='Status: true or false', required=True)
@click.pass_context
@has_permission(['management'])
def create_contract(ctx, client, management, total, remain, status):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        status = True if status == 'true' else False

        client_found = False
        client_list = session.scalars(select(Client).order_by(Client.id)).all()
        for element in client_list:
            if element.id == int(client):
                client = element.id
                client_found = True

        if not client_found:
            return client_not_found(client)

        commercial_found = False
        commercial_list = session.scalars(select(User).order_by(User.id)).all()
        for element in commercial_list:
            if element.id == int(management) and element.role.name == "commercial":
                management = element.id
                commercial_found = True

        if not commercial_found:
            return user_not_found(management)

        new_contract = Contract(client_id=client, uuid=str(uuid.uuid4()), management_contact_id=management,
                                total_amount=total, remaining_amount=remain,
                                status=status)

        session.add(new_contract)
        session.commit()
        created_succes(new_contract)

    except KeyError:
        invalid_token()
        pass


@contract.command()
@click.option('--id', '-i', help='Contract ID')
@click.option('--client', '-c', help='Client ID')
@click.option('--management', '-m', help='Management ID')
@click.option('--total', '-ta', help='Total Amount')
@click.option('--remain', '-r', help='Remaining Amount')
@click.option('--status', '-s', help='Status: true or false')
@click.pass_context
@has_permission(['management', 'commercial'])
def modify_contract(ctx, id, client, management, total, remain, status):
    session = ctx.obj['session']

    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        contract_to_modify = session.scalar(
            select(Contract).where(Contract.id == id))

        if contract_to_modify:

            if client is not None:
                client_found = False
                client_list = session.scalars(select(Client).order_by(Client.id)).all()
                for element in client_list:
                    if element.id == int(client):
                        contract_to_modify.client_id = element.id
                        client_found = True

                if not client_found:
                    return client_not_found(client)

            if management is not None:
                commercial_found = False
                commercial_list = session.scalars(select(User).order_by(User.id)).all()
                for element in commercial_list:
                    if element.id == int(management) and element.role.name == "commercial":
                        contract_to_modify.management_contact_id = element.id
                        commercial_found = True

                if not commercial_found:
                    return user_not_found(management)

            if total is not None:
                contract_to_modify.total_amount = total

            if remain is not None:
                contract_to_modify.remaining_amount = remain

            if status is not None:
                status = True if status == 'true' else False
                contract_to_modify.status = status

            session.commit()
            modification_done(contract_to_modify)
        else:
            contract_not_found(id)

    except KeyError:
        invalid_token()
        pass


@contract.command()
@click.option('--id', '-i', help='Id of the contract you want to delete',
              required=True)
@click.pass_context
@has_permission(['management', 'commercial'])
def delete_contract(ctx, id):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        contract_to_delete = session.scalar(
            select(Contract).where(Contract.id == id))

        if contract_to_delete:
            session.delete(contract_to_delete)
            session.commit()
            deleted_success(id, contract_to_delete)

        else:
            contract_not_found(id)

    except KeyError:
        invalid_token()
        pass