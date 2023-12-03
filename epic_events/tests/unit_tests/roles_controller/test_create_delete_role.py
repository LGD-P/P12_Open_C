from sqlalchemy import select

from epic_events.controllers.roles_controller import create_role
from epic_events.models.user import User



def test_create_roles(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(create_role, ["-i", "1", '-n', 'support'],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
    })

    assert result.exit_code == 0
    assert "\n 'SUPPORT'created successfully.\n\n" in result.output
