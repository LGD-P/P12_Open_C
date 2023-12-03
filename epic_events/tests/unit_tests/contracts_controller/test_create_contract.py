from sqlalchemy import select
from epic_events.models.contract import Contract
from epic_events.models.user import User
from epic_events.controllers.contracts_controller import create_contract


def test_create_contract(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(
        create_contract,
        ["-c", "2", "-m", "2", "-ta", "2000", "-r", "1000", "-s", "true"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    assert result.exit_code == 0
    contract = mocked_session.scalar(select(Contract).where(Contract.id == 4))

    assert f"\n ID N° 'N°4' Contract 'N°{str(contract.uuid)}'created \nsuccessfully.\n\n" in result.output


def test_create_contract_with_wrong_client_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(
        create_contract,
        ["-c", "12", "-m", "3", "-ta", "2000", "-r", "1000", "-s", "true"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    assert result.exit_code == 1
    assert "\n Client with ID '12' is 'not found'.\n\n" in result.output


def test_create_contract_without_authentication(runner, mocked_session):
    result = runner.invoke(
        create_contract,
        ["-c", "2", "-m", "3", "-ta", "2000", "-r", "1000", "-s", "true"],
        catch_exceptions=KeyError,
        obj={
            "session": mocked_session,
        })

    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
    assert result.exit_code == 0


def test_create_contract_without_permission(runner, mocked_session):
    user_logged_as_support = mocked_session.scalar(select(User).where(User.id == 1))
    result = runner.invoke(
        create_contract,
        ["-c", "2", "-m", "3", "-ta", "2000", "-r", "1000", "-s", "true"],
        obj={
            "session": mocked_session,
            "user_id": user_logged_as_support
        })

    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0


def test_create_contract_with_missing_argument(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(
        create_contract,
        ["-c", "2", "-m", "3", "-ta", "2000", "-r", "-s", "true"],
        obj={
            "session": mocked_session,
            "user_id": user_logged
        })

    assert result.exit_code == 2
    assert "Missing option '--status' / '-s'" in result.output
