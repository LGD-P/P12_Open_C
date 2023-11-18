from sqlalchemy import select
from epic_events.models.contract import Contract
from epic_events.models.user import User
from epic_events.controllers.contracts_controller import delete


def test_delete_contrat(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    contract_to_delete = mocked_session.scalar(select(Contract).where(Contract.id == 3))

    uuid = contract_to_delete.uuid
    result = runner.invoke(delete, ["-i", "3"],
                           obj={"session": mocked_session,
                                "user_id": user_logged})

    assert mocked_session.scalar(select(Contract).where(Contract.id == 3)) is None
    assert result.exit_code == 0
    assert f"\n Client with ID '3', UUID 'N°{uuid}' has been \n'deleted'.\n\n" in result.output


def test_delete_contrat_with_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))

    result = runner.invoke(delete, ["-i", "12"],
                           obj={"session": mocked_session,
                                "user_id": user_logged})
    assert result.exit_code == 0
    assert f"\n Contract with ID '12' is 'not found'.\n" in result.output


def test_delete_contrat_without_authentication(runner, mocked_session):
    result = runner.invoke(delete, ["-i", "12"],
                           obj={"session": mocked_session})

    assert result.exit_code == 0
    assert "\n' Invalid Token  please logged in again' \n" in result.output


def test_delete_contrat_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))

    result = runner.invoke(delete, ["-i", "3"],
                           obj={"session": mocked_session,
                                "user_id": user_logged})

    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0
