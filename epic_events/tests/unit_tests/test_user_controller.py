from sqlalchemy import select

from epic_events.controllers.user_controller import list_user
from epic_events.models.user import User


def test_list(runner, mocked_session):
    user = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(list_user, obj={"session":mocked_session, "user_id":user})
    assert result.exit_code == 0
    assert  "1  │ Kevin  │ keven@epicevent.com  │  ID : 1 - type : support    │ ****  " in result.output
