from sqlalchemy import select
from epic_events.models.user import User
from epic_events.controllers.contracts_controller import list_contract


def test_list_all_contracts(runner, mocked_session):
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


def test_list_all_unsigned_contracts_for_commercial_team(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(list_contract, ["-ns"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert '│ 2  │ 374e557… │    2     │    3     │   1051   │  3671   │ 2023-11… │   ❌ ' in result.output
    assert result.exit_code == 0


def test_list_all_signed_contracts_for_commercial_team(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 3))
    result = runner.invoke(list_contract, ['-s'],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    print(result.output)
    assert '│ 1  │ d707c9f… │    1     │    3     │  13757   │   227   │ 2023-07… │   ✅ ' in result.output
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


def test_list_single_contract_wrong_id(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_contract, ["-i", "13"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n Contract with ID '13' is 'not found'.\n" in result.output
    assert result.exit_code == 1


def test_list_single_contract_without_permission(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 1))
    result = runner.invoke(list_contract, ["-i", "1"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    assert "\n' You're not allowed to use this command'\n\n" in result.output
    assert result.exit_code == 0


def test_list_contract_without_authentication(runner, mocked_session):
    result = runner.invoke(list_contract, ["-i", "1"],
                           obj={
                               "session": mocked_session,

                           })

    assert "\n' Invalid Token  please logged in again' \n\n" in result.output
    assert result.exit_code == 0
