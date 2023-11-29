from epic_events.models.client import Client
from epic_events.models.user import User
from epic_events.models.contract import Contract
from epic_events.utils import find_user_type, find_client_or_contract
from epic_events.utils import has_permission
from epic_events.views.users_view import logged_as, invalid_token
from epic_events.views.contracts_views import (contracts_table, created_succes,
                                               deleted_success, contract_not_found,
                                               modification_done, not_in_charge_of_this_client_contract,
                                               sentry_contract_created_and_signed, sentry_contract_status_signed)

import rich_click as click
from sqlalchemy import select
import uuid
import sentry_sdk
from sentry_sdk import capture_message


@click.group()
@click.pass_context
def contract(ctx):
    """Allows the MANAGEMENT & COMMERCIAL, within the limits of their permissions,
     to access various operations of the Contracts CRUD ."""
    pass


@contract.command()
@click.option("--id", "-i", help="id of the event to search", )
@click.option("--signed", "-s", is_flag=True, help="For Commercial-Team Only signed contract", )
@click.option("--is_not_signed", "-ns", is_flag=True, help="For Commercial-Team Only not signed contract", )
@click.pass_context
@has_permission(['management', 'commercial'])
def list_contract(ctx, id, signed, is_not_signed):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(select(User).where(User.id == ctx.obj['user_id'].id))
        if id:
            selected_contract = session.scalar(
                select(Contract).where(Contract.id == id))

            if selected_contract is None:
                raise click.UsageError(contract_not_found(id))
            else:
                contracts_table([selected_contract])
        if is_not_signed:
            contract_list = session.scalars(select(Contract).where(Contract.status.is_(None))).all()
            contracts_table(contract_list)

        if signed:
            contract_list = session.scalars(select(Contract).where(Contract.status)).all()
            contracts_table(contract_list)
        else:
            contract_list = session.scalars(
                select(Contract).order_by(Contract.id)).all()

            contracts_table(contract_list)
            logged_as(user_logged.name, user_logged.role.name)

    except KeyError:
        message = invalid_token()
        sentry_sdk.capture_exception(message)

    except Exception as e:
        sentry_sdk.capture_exception(e)


@contract.command()
@click.option('--client', '-c', help='Client ID', required=True)
@click.option('--management', '-m', help='Management ID', required=True)
@click.option('--total', '-ta', help='Total Amount', required=True)
@click.option('--remain', '-r', help='Remaining Amount', required=True)
@click.option('--status', '-s', help='Status: true or false', required=True)
@click.pass_context
@has_permission(['management'])
def create_contract(ctx, client, management, total, remain, status):
    session = ctx.obj['session']
    try:
        user_logged = session.scalar(select(User).where(User.id == ctx.obj['user_id'].id))

        status = True if status.lower() == 'true' else False

        client_found = find_client_or_contract(ctx, Client, client)

        commercial_found = find_user_type(ctx, management, 'management')

        new_contract = Contract(client_id=client_found, uuid=str(uuid.uuid4()), management_contact_id=commercial_found,
                                total_amount=total, remaining_amount=remain,
                                status=status)

        session.add(new_contract)
        session.commit()
        created_succes(new_contract)
        if new_contract.status is True:
            sentry_sdk.set_context("create_contract", {
                "contract": new_contract,
                "created_by": user_logged})

            capture_message(sentry_contract_created_and_signed(user_logged, new_contract))

    except KeyError:
        message = invalid_token()
        sentry_sdk.capture_exception(message)

    except Exception as e:
        sentry_sdk.capture_exception(e)


@contract.command()
@click.option('--id', '-i', help='Contract ID')
@click.option('--client', '-c', help='Client ID')
@click.option('--management', '-m', help='Management ID')
@click.option('--total', '-ta', help='Total Amount')
@click.option('--remain', '-r', help='Remaining Amount')
@click.option('--status', '-s', help='Status: true or false')
@click.pass_context
@has_permission(['management', 'commercial'])
def modify_contract(ctx, id, client, management, total, remain, status):
    session = ctx.obj['session']

    try:
        user_logged = session.scalar(
            select(User).where(User.id == ctx.obj['user_id'].id))

        contract_to_modify = session.scalar(
            select(Contract).where(Contract.id == id))

        if contract_to_modify:
            if user_logged.role.name == "commercial":
                if contract_to_modify.total_amount == user_logged.id:
                    pass
                else:
                    raise ValueError(not_in_charge_of_this_client_contract(contract_to_modify.client_id))

            if client is not None:
                client_found = find_client_or_contract(ctx, Client, client)
                contract_to_modify.client_id = client_found

            if management is not None:
                commercial_found = find_user_type(ctx, management, 'management')
                contract_to_modify.management_contact_id = commercial_found

            if total is not None:
                contract_to_modify.total_amount = total

            if remain is not None:
                contract_to_modify.remaining_amount = remain

            if status is not None:
                status = True if status == 'true' else False
                contract_to_modify.status = status
                if status is True:
                    sentry_sdk.set_context("create_contract", {
                        "contract": contract_to_modify,
                        "created_by": user_logged})

                    capture_message(sentry_contract_status_signed(user_logged, contract_to_modify))

            session.commit()
            modification_done(contract_to_modify)

        else:
            raise click.UsageError(contract_not_found(id))

    except KeyError:
        message = invalid_token()
        sentry_sdk.capture_exception(message)

    except Exception as e:
        sentry_sdk.capture_exception(e)


@contract.command()
@click.option('--id', '-i', help='Id of the contract you want to delete',
              required=True)
@click.pass_context
@has_permission(['management', 'commercial'])
def delete_contract(ctx, id):
    session = ctx.obj['session']
    try:
        session.scalar(select(User).where(User.id == ctx.obj['user_id'].id))

        contract_to_delete = session.scalar(
            select(Contract).where(Contract.id == id))

        if contract_to_delete:
            session.delete(contract_to_delete)
            session.commit()
            deleted_success(id, contract_to_delete)

        else:
            raise click.UsageError(contract_not_found(id))

    except KeyError:
        message = invalid_token()
        sentry_sdk.capture_exception(message)

    except Exception as e:
        sentry_sdk.capture_exception(e)
