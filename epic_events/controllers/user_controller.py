from models.models import (User, session)
from views.users_view import (
    users_table, created_succes, deleted_success, user_not_found,
    table_not_found, param_required, invalid_email, invalid_pass, invalid_role, modification_done)
import re
import passlib.hash
import psycopg2
import click


class UserApp():
    @staticmethod
    def pass_is_valid(ctx, param, value):
        regex = re.compile(
            "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
        if value != ctx.params.get('password', None) and re.fullmatch(regex, value) is None:
            invalid_pass()
            raise click.UsageError(
                "Invalid password. Passwords do not match or not strong enough.")
        return value

    @staticmethod
    def email_is_valid(ctx, param, value):
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9-]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, value):
            return value
        else:
            invalid_email()
            raise click.UsageError("Invalid email.")

    @staticmethod
    def role_is_valid(ctx, param, value):

        if value in ["support", "commercial", "management"]:
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
    def access_users(ctx, table):
        conn = ctx.obj['conn']

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
    def create_user(ctx, table, name, email, role, password):
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
                created_succes(new_user)

        cur.close()
        conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to query', required=True)
    @click.option('--id', '-i', help='Id of the user you want to modify', required=True)
    @click.option('--name', '-n', help='New name of the user')
    @click.option('--email', '-e', help='New email of the user')
    @click.option('--role', '-r', help='New role of the user, must be: support management or commercial')
    # Modification du password à faire
    @click.pass_context
    def modify_user(ctx, table, id, name, email, role):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'users':
            user_to_modify = session.query(User).filter_by(id=id).first()

            if user_to_modify:

                if name is not None:
                    user_to_modify.name = name
                if email is not None:
                    email = UserApp.email_is_valid(ctx, None, email)
                    user_to_modify.email = email

                if role is not None:
                    role = UserApp.role_is_valid(ctx, None, role)
                    user_to_modify.role = role

                """
                if password is not None:
                    password = UserApp.pass_is_valid(ctx, None, password)
                    user_to_modify.password = passlib.hash.argon2.using(
                        rounds=12).hash(password)
                """

                session.commit()
                modification_done(user_to_modify)
            else:
                user_not_found(id)
        else:
            table_not_found(table)

        cur.close()
        conn.close()

    @connect.command()
    @click.option('--table', '-t', help='Name of the table to query', required=True)
    @click.option('--id', '-i', help='Id of the user you want to delete', required=True)
    @click.pass_context
    def delete_user(ctx, table, id):
        conn = ctx.obj['conn']
        cur = conn.cursor()

        if table == 'users':
            user_to_delete = session.query(User).filter_by(id=id).first()

            if user_to_delete:
                session.delete(user_to_delete)
                session.commit()
                deleted_success(id, user_to_delete)

            else:
                user_not_found(id)
        else:
            table_not_found(table)
        cur.close()
        conn.close()
