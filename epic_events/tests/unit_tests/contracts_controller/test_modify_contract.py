from sqlalchemy import select
from epic_events.models.contract import Contract
from epic_events.models.user import User
from epic_events.controllers.contracts_controller import modify_contract


def test_modify_contract_client(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(
        modify_contract,
        ["-i", "1", "-c", "2"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    new_contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    assert new_contract.client_id != 1
    assert new_contract.client_id == 2
    assert f"\n Contract 'N°{str(new_contract.uuid)}' successfully modified.\n\n"
    assert result.exit_code == 0


def test_modify_contract_client_with_wrong_commercial(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(
        modify_contract,
        ["-i", "1", "-m", "12"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    assert "\n User with ID '12' is 'not found'.\n\n"
    assert result.exit_code == 1


def test_modify_contract_total_amount(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    old_contract_client_id = contract.total_amount
    result = runner.invoke(
        modify_contract,
        ["-i", "1", "-ta", "50000"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    new_contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    assert new_contract.total_amount != old_contract_client_id
    assert new_contract.total_amount == 50000
    assert result.exit_code == 0


def test_modify_contract_remaining_amount(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    old_contract_client_id = contract.remaining_amount
    result = runner.invoke(
        modify_contract,
        ["-i", "1", "-r", "10000"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    new_contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    assert new_contract.remaining_amount != old_contract_client_id
    assert new_contract.remaining_amount == 10000
    assert result.exit_code == 0


def test_modify_contract_status(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    contract_to_modify = mocked_session.scalar(select(Contract).where(Contract.id == 2))
    old_contract_client_id = contract_to_modify.status
    result = runner.invoke(
        modify_contract,
        ["-i", "2", "-s", "true"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    assert contract_to_modify.status != old_contract_client_id
    assert contract_to_modify.status is True
    assert result.exit_code == 0


def test_modify_contract_client_without_authentication(runner, mocked_session):
    result = runner.invoke(
        modify_contract,
        ["-i", "1", "-c", "2"],
        obj={
            "session": mocked_session,

        })
    assert result.exit_code == 0
    assert "\n' Invalid Token  please logged in again' \n" in result.output


def test_modify_contract_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))
    result = runner.invoke(
        modify_contract,
        ["-i", "1", "-c", "2"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })
    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0


def test_commercial_modify_contract_but_not_charge_of_client(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 6))
    result = runner.invoke(
        modify_contract,
        ["-i", "1", "-c", "2"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    assert "\n' YAs commercial you are 'not in charge' of Client : ID '1'. You're 'not allowed' "
    "to modify this Contract.\n\n" in result.output
    assert result.exit_code == 1
