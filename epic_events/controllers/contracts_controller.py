from epic_events.models.contract import Contract
from epic_events.views.contracts_views import (contracts_table, created_succes, deleted_success,
                                               contract_not_found, modification_done)

import click

from sqlalchemy import select


@click.group()
@click.pass_context
def contract(ctx):
    pass


@contract.command()
@click.option("--id", "-i", help="id of the event to search", )
@click.pass_context
def list(ctx, id):
    session = ctx.obj['session']

    if id:
        contract = session.scalar(select(Contract).where(Contract.id == id))
        if contract is None:
            contract_not_found(id)
        else:
            contracts_table([contract])
    else:
        contract_list = session.scalars(
            select(Contract).order_by(Contract.id)).all()

        contracts_table(contract_list)


@contract.command()
@click.option('--client', '-c', help='Client ID', required=True)
@click.option('--management', '-m', help='Management ID', required=True)
@click.option('--total', '-ta', help='Total Amount', required=True)
@click.option('--remain', '-r', help='Remaining Amount', required=True)
@click.option('--status', '-s', help='Status: true or false', required=True)
@click.pass_context
def create(ctx, client, management, total, remain, status):
    session = ctx.obj['session']

    status = True if status == 'true' else False
    new_contract = Contract(client_id=client, management_contact_id=management,
                            total_amount=total, remaining_amount=remain,
                            status=status)

    session.add(new_contract)
    session.commit()
    created_succes(new_contract)


@contract.command()
@click.option('--id', '-i', help='Contract ID')
@click.option('--client', '-c', help='Client ID')
@click.option('--management', '-m', help='Management ID')
@click.option('--total', '-ta', help='Total Amount')
@click.option('--remain', '-r', help='Remaining Amount')
@click.option('--status', '-s', help='Status: true or false')
@click.pass_context
def modify(ctx, id, client, management, total, remain, status):
    session = ctx.obj['session']

    contract_to_modify = session.scalar(
        select(Contract).where(Contract.id == id))

    if contract_to_modify:

        if client is not None:
            contract_to_modify.client_id = client
        if management is not None:
            contract_to_modify.management_contact_id = management

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


@contract.command()
@click.option('--id', '-i', help='Id of the contract you want to delete', required=True)
@click.pass_context
def delete(ctx, id):
    session = ctx.obj['session']

    contract_to_delete = session.scalar(
        select(Contract).where(Contract.id == id))

    if contract_to_delete:
        session.delete(contract_to_delete)
        session.commit()
        deleted_success(id, contract_to_delete)

    else:
        contract_not_found(id)
