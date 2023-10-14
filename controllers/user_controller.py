from models.models import (User, Client, Contract, Event, session)
from views.users_view import (
    users_table, created_succes, deleted_success, user_not_found,
    table_not_found, param_required, invalid_email, invalid_pass,invalid_role)
import re
import passlib.hash
import psycopg2
import click

from rich.console import Console
from rich.table import Table
from rich.text import Text


class UserApp():
    
    
    
    
    def pass_is_valid(ctx, param, value):
        regex = re.compile(
            "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
        if value != ctx.params.get('password', None) and re.fullmatch(regex, value) is None:
            invalid_pass()
            raise click.UsageError(
                "Invalid password. Passwords do not match or not strong enough.")
        return value


    def email_is_valid(ctx, param, value):
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9-]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, value):
            return value
        else:
            invalid_email()
            raise click.UsageError("Invalid email.")
        
        

    def role_is_valid(ctx, param, value):
    
        if value in ["support", "commercial" ,"management"]:
            return value
        else:
            invalid_role()
            raise click.UsageError("Invalid role")
            
    
    

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
    def read_all_in_table(ctx, table):
        conn = ctx.obj['conn']
        imported_session = session

        if table == 'users':
            users = session.query(User).all()
            users_table(users, table)
            session.close()
        else:
            table_not_found(table)

        conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to create in', required=True)
    @click.option('--name', '-n', help='Name for the new object', required=True)
    @click.option('--email', '-e', help='Email for the new object', required=True, callback=email_is_valid)
    @click.option('--role', '-r', help='Role must be : support management or commercial', required=True, callback=role_is_valid)
    @click.option('--password', '-P', prompt=True, hide_input=True, confirmation_prompt=True, required=True,
                  callback=pass_is_valid)
    @click.pass_context
    def create(ctx, table, name, email, role, password):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'users':
            if not name or not email or not role:
                param_required()
            else:
                
                hashed_password = passlib.hash.argon2.using(
                    rounds=12).hash(password)

                new_user = User(name=name, email=email,
                                role=role, password=hashed_password)
                session.add(new_user)
                session.commit()
                created_succes()

        cur.close()
        conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to query', required=True)
    @click.option('--id', '-i', help='Id of the user you want to delete', required=True)
    @click.pass_context
    def delete_in_table(ctx, table, id):
        conn = ctx.obj['conn']

        if table == 'users':
            user_to_delete = session.query(User).filter_by(id=id).first()

            if user_to_delete:
                session.delete(user_to_delete)
                session.commit()
                deleted_success(id)

            else:
                user_not_found(id)
        else:
            table_not_found(table)
