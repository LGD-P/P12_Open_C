from epic_events.models.models import Contract
from epic_events.views.contracts_views import (contracts_table, param_required,
                                               created_succes, deleted_success, contract_not_found,
                                               modification_done)

import click

from sqlalchemy import select


@click.group()
@click.pass_context
def contract(ctx):
    pass


@contract.command()
@click.option("--id", "-i", help="id of the contact search", )
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


"""
@contract.command()
@click.option('--table', '-t', help='Name of the table to create in', required=True)
@click.option('--client', '-c', help='Client ID', required=True)
@click.option('--management', '-m', help='Management ID', required=True)
@click.option('--total', '-ta', help='Total Amount', required=True)
@click.option('--remain', '-r', help='Remaining Amount', required=True)
@click.option('--status', '-s', help='Status: true or false', required=True)
@click.pass_context
def create_contract(ctx, table, client, management, total, remain, status):
    conn = ctx.obj['conn']
    cur = conn.cursor()

    if table == 'contracts':
        if not client or not management or not total or not remain or not status:
            param_required()
        else:
            status = True if status == 'true' else False
            new_contract = Contract(client_id=client, management_contact_id=management,
                                    total_amount=total, remaining_amount=remain,
                                    status=status)

            session.add(new_contract)
            session.commit()
            created_succes(new_contract)

    cur.close()
    conn.close()


@contract.command()
@click.option('--table', '-t', help='Name of the table to create in', required=True)
@click.option('--id', '-i', help='Contract ID')
@click.option('--client', '-c', help='Client ID')
@click.option('--management', '-m', help='Management ID')
@click.option('--total', '-ta', help='Total Amount')
@click.option('--remain', '-r', help='Remaining Amount')
@click.option('--status', '-s', help='Status: true or false')
@click.pass_context
def modify_contract(ctx, table, id, client, management, total, remain, status):
    conn = ctx.obj['conn']
    cur = conn.cursor()

    if table == 'contracts':
        contract_to_modify = session.query(
            Contract).filter_by(id=id).first()

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
                contract_to_modify.status = status

            session.commit()
            modification_done(contract_to_modify)
        else:
            contract_not_found(id)
    else:
        table_not_found(table)

    cur.close()


@contract.command()
@click.option('--table', '-t', help='Name of the table to query', required=True)
@click.option('--id', '-i', help='Id of the contract you want to delete', required=True)
@click.pass_context
def delete_contract(ctx, table, id):
    conn = ctx.obj['conn']
    cur = conn.cursor()

    if table == 'contracts':
        contract_to_delete = session.query(
            Contract).filter_by(id=id).first()

        if contract_to_delete:
            session.delete(contract_to_delete)
            session.commit()
            deleted_success(id, contract_to_delete)

        else:
            contract_not_found(id)
    else:
        table_not_found(table)
    cur.close()
    conn.close()
"""
