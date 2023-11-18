from sqlalchemy import select
from epic_events.models.contract import Contract
from epic_events.models.user import User
from epic_events.controllers.contracts_controller import list_contract


# Affiner le result.output avec le débugger
# Modifier le controller try except
def test_list_contract(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_contract,
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert '13757' in result.output
    assert '1051' in result.output
    assert '8664' in result.output
    assert result.exit_code == 0


def test_list_single_contract(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_contract, ["-i", "1"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert '13757' in result.output
    assert result.exit_code == 0


def test_list_signle_contract_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_contract, ["-i", "13"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n Contract with ID '13' is 'not found'.\n" in result.output
    assert result.exit_code == 0


def test_list_signle_contract_not_allowed(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))
    result = runner.invoke(list_contract, ["-i", "1"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0

    def test_list_contract_without_athentication(runner, mocked_session):
        result = runner.invoke(list_contract, ["-i", "1"],
                               obj={
                                   "session": mocked_session,

                               })

        assert "\n' Invalid Token  please logged in again' \n\n" in result.output
        assert result.exit_code == 0
