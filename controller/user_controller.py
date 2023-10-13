from models.models import (User, Client, Contract, Event, session)
import re
import passlib.hash

import psycopg2
import click
from rich.console import Console
from rich.table import Table
from rich.text import Text


class App():

    def pass_is_valid(ctx, param, value):
        regex = re.compile(
            "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
        if value != ctx.params.get('password', None) and re.fullmatch(regex, value) is None:
            raise click.UsageError(
                "Invalid password. Passwords do not match or not strong enough.")
        return value

    def email_is_valid(ctx, param, value):
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9-]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, value):
            return value
        else:
            raise click.UsageError("Invalid email address.")

    @staticmethod
    def create_user_table(users, table):
        console = Console()

        user_table = Table(show_header=True, header_style="bold blue",
                           title=f'[bold red]Table: {table}[/bold red]')
        user_table.add_column(
            Text("ID", style="bleu", justify="center", no_wrap=True), justify="left", style="green",
        )
        user_table.add_column(
            Text("Name", style="blue", justify="center", no_wrap=True), justify="left", style="green"
        )
        user_table.add_column(
            Text("Email", style="blue", justify="center", no_wrap=True), justify="left", style="green"
        )
        user_table.add_column(
            Text("Role", style="blue", justify="center", no_wrap=True), justify="left", style="green"
        )
        user_table.add_column(
            Text("Password", style="blue", justify="center", no_wrap=True), justify="left", style="red"
        )

        for user in users:
            user.password = "****" if "$argon2" in user.password else user.password
            user_table.add_row(
                str(user.id),
                user.name,
                user.email,
                user.role,
                user.password
            )

        console.print(user_table)

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
    @click.option('--table', '-t', help='Name of the table to query')
    @click.pass_context
    def read_all_in_table(ctx, table):
        conn = ctx.obj['conn']
        imported_session = session

        if table == 'users':

            users = session.query(User).all()
            App.create_user_table(users, table)
            session.close()
        else:
            click.echo(f"Table '{table}' not found")

        conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to create in')
    @click.option('--name', '-n', help='Name for the new object')
    @click.option('--email', '-e', help='Email for the new object', callback=email_is_valid)
    @click.option('--role', '-r', help='Role for the new user')
    @click.option('--password', '-P', prompt=True, hide_input=True, confirmation_prompt=True,
                  callback=pass_is_valid)
    @click.pass_context
    def create(ctx, table, name, email, role, password):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'users':
            if not name or not email or not role:
                click.echo(
                    "Name, email, and role are required for user creation.")
            else:
                hashed_password = passlib.hash.argon2.using(
                    rounds=12).hash(password)

                new_user = User(name=name, email=email,
                                role=role, password=hashed_password)
                session.add(new_user)
                session.commit()
                click.echo("User created successfully.")

        cur.close()
        conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to query')
    @click.option('--id', '-i', help='Id of the user you want to delete')
    @click.pass_context
    def delete_in_table(ctx, table, id):
        conn = ctx.obj['conn']
        cur = conn.cursor()
        cur.execute(f'DELETE FROM {table} WHERE id = %s;', (id,))
        conn.commit()
        cur.close()
        conn.close()
