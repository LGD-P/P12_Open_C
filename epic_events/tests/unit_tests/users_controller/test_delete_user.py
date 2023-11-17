from sqlalchemy import select
from sqlalchemy.orm import session

from epic_events.controllers.user_controller import delete
from epic_events.models.user import User


def test_delete_user(runner, mocked_session):
  user_logged = mocked_session.scalar(select(User).where(User.id == 2))

  result = runner.invoke(delete, ["-i", "3"],
                         obj={
                             "session": mocked_session,
                             "user_id": user_logged
                         })

  assert "\n User with ID '3', 'PIERRE' has been 'deleted'.\n\n" in result.output
  assert result.exit_code == 0



def test_delete_user_wrong_id(runner, mocked_session):
  user_logged = mocked_session.scalar(select(User).where(User.id == 2))

  result = runner.invoke(delete, ["-i", "6"],
                         obj={
                             "session": mocked_session,
                             "user_id": user_logged
                         })

  assert "\n User with ID '6' is 'not found'.\n\n" in result.output
  assert result.exit_code == 0




def test_delete_user_without_perm(runner, mocked_session):
  user_logged = mocked_session.scalar(select(User).where(User.id == 1))

  result = runner.invoke(delete, ["-i", "2"],
                         obj={
                             "session": mocked_session,
                             "user_id": user_logged
                         })

  assert "\n' You're not allowed to use this command'\n\n" in result.output
  assert result.exit_code == 0