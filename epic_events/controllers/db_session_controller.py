from functools import update_wrapper
import psycopg2
import click


def pass_obj(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        return ctx.invoke(f, ctx.obj, *args, **kwargs)
    return update_wrapper(new_func, f)


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
