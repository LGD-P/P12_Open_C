import psycopg2
import click


def get_db_conn(host, port, user, password, dbname):
    """This function is used to connect controller to db in docker
    """
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname
    )
    return conn


@click.command()
@click.option('--table', '-t', help='Name of the table to query')
@click.option('--host', '-h', default='localhost', help='Database host')
@click.option('--port', '-p', default=5432, help='Database port')
@click.option('--user', '-u', default='postgres', help='Database user')
@click.option('--password', '-P', default='MyPassIs23Word', help='Database password')
@click.option('--dbname', '-d', default='postgres', help='Database name')
def query_table(table, host, port, user, password, dbname):
    conn = get_db_conn(host, port, user, password, dbname)
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table};')
    rows = cur.fetchall()
    for row in rows:
        click.echo(row)
    cur.close()
    conn.close()


query_table()
