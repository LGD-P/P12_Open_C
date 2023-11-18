from sqlalchemy import select
from epic_events.models.contract import Contract
from epic_events.models.user import User
from epic_events.controllers.contracts_controller import modify


def test_modify_contract_client(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    old_contract_client_id = contract.client_id
    result = runner.invoke(
        modify,
        ["-i", "1", "-c", "2"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    new_contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    assert new_contract.client_id != old_contract_client_id
    assert new_contract.client_id == 2
    assert result.exit_code == 0


def test_modify_contract_total_amount(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    old_contract_client_id = contract.total_amount
    result = runner.invoke(
        modify,
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
        modify,
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
    contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    old_contract_client_id = contract.status
    result = runner.invoke(
        modify,
        ["-i", "1", "-s", "true"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    new_contract = mocked_session.scalar(select(Contract).where(Contract.id == 1))
    assert new_contract.status != old_contract_client_id
    assert new_contract.status == True
    assert result.exit_code == 0
