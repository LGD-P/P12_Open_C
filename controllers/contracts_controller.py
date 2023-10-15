from models.models import Contract, session
from views.contracts_views import (contracts_table, table_not_found, param_required,
                                   created_succes, deleted_success, contract_not_found,
                                   modification_done)


import psycopg2
import click


class ContractApp():

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
    def access_contracts(ctx, table):
        conn = ctx.obj['conn']
        session

        if table == 'contracts':
            contracts = session.query(Contract).all()
            contracts_table(contracts, table)
            session.close()
        else:
            table_not_found(table)

        conn.close()

    @connect.command()
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

    @connect.command()
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

    @connect.command()
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
