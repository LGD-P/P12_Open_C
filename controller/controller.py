from models.models import (User, Client, Contract, Event)

import psycopg2
import click


class App():

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
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {table};')
        rows = cur.fetchall()
        for row in rows:
            click.echo(row)
        cur.close()
        conn.close()


"""
if __name__ == '__main__':
    app = App.cli(obj={})
"""
