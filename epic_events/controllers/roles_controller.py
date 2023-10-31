from epic_events.models.role import Role
from epic_events.models.user import User
from epic_events.views.roles_views import (
    id_not_found, role_not_found, roles_table, created_succes, deleted_success)


import click
from sqlalchemy import select


@click.group()
@click.pass_context
def role(ctx):
    pass


@role.command()
@click.option('--id', '-i', help='Name of the table to query', required=False)
@click.pass_context
def list(ctx, id):
    session = ctx.obj['session']
    if id:
        role = session.scalar(select(Role).where(Role.id == id))
        if role is None:
            role_not_found(id)
        else:
            roles_table([role])
    else:
        roles_list = session.scalars(
            select(Role).order_by(Role.id)).all()

        roles_table(roles_list)


@role.command()
@click.option('--name', '-n', help='Must be "support" "commercial" or "manager"', required=True)
@click.option('--id', '-i', help='Full name for the new object', required=True)
@click.pass_context
def create(ctx, name, id):
    session = ctx.obj['session']

    is_id = session.scalar(select(User).where(
        User.id == id)) if id is not None else None

    if Role.role_is_valid(ctx, name):
        if is_id is not None:
            print(is_id)
            print(id)
            new_role = Role(name=name)
            print(new_role)
            new_role.users.append(is_id)
            session.add(new_role)
            session.commit()
            created_succes(new_role)
        else:
            id_not_found(id)


"""
@role.command()
@click.option('--id', '-i', help='Id of the user you want to modify', required=True)
@click.option('--name', '-n', help='Full name for the new object')
@click.option('--email', '-e', help='Email for the new object')
@click.option('--phone', '-ph', help='Phone nummber')
@click.option('--company', '-c', help='Company name')
@click.pass_context
def modify(ctx, id, name, email, phone, company):
    session = ctx.obj['session']

    role_to_modify = session.scalar(select(Role).where(Role.id == id))

    if role_to_modify:

        if name is not None:
            role_to_modify.full_name = name
        if email is not None:
            role_to_modify.email = email

        session.commit()
        modification_done(role_to_modify)
    else:
        role_not_found(id)
"""


@role.command()
@click.option('--id', '-i', help='Id of the role you want to delete', required=True)
@click.pass_context
def delete(ctx, id):
    session = ctx.obj['session']

    role_to_delete = session.scalar(select(Role).where(Role.id == id))

    if role_to_delete:
        session.delete(role_to_delete)
        session.commit()
        deleted_success(id, role_to_delete)

    else:
        role_not_found(id)
