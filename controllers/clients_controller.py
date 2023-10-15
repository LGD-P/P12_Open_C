from models.models import (Client, session)
from views.clients_views import (
    clients_table, table_not_found, param_required, created_succes,
    deleted_success, client_not_found, modification_done)

from datetime import datetime
import psycopg2
import click


class ClientApp():

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
    def access_clients(ctx, table):
        conn = ctx.obj['conn']
        session

        if table == 'clients':
            clients = session.query(Client).all()
            clients_table(clients, table)
            session.close()
        else:
            table_not_found(table)

        conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to create in', required=True)
    @click.option('--name', '-n', help='Full name for the new object', required=True)
    @click.option('--email', '-e', help='Email for the new object', required=True)
    @click.option('--phone', '-ph', help='Phone nummber', required=True)
    @click.option('--company', '-c', help='Company name')
    @click.pass_context
    def create_client(ctx, table, name, email, phone, company):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'clients':
            if not name or not email or not phone:
                param_required()
            else:
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

        cur.close()
        conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to query', required=True)
    @click.option('--id', '-i', help='Id of the user you want to modify', required=True)
    @click.option('--name', '-n', help='Full name for the new object')
    @click.option('--email', '-e', help='Email for the new object')
    @click.option('--phone', '-ph', help='Phone nummber')
    @click.option('--company', '-c', help='Company name')
    @click.pass_context
    def modify_client(ctx, table, id, name, email, phone, company):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'clients':
            client_to_modify = session.query(Client).filter_by(id=id).first()

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
        else:
            table_not_found(table)

        cur.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to query', required=True)
    @click.option('--id', '-i', help='Id of the user you want to delete', required=True)
    @click.pass_context
    def delete_client(ctx, table, id):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'clients':
            client_to_delete = session.query(Client).filter_by(id=id).first()

            if client_to_delete:
                session.delete(client_to_delete)
                session.commit()
                deleted_success(id, client_to_delete)

            else:
                client_not_found(id)
        else:
            table_not_found(table)
        cur.close()
        conn.close()
