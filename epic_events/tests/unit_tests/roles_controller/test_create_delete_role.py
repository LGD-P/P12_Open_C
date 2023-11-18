from sqlalchemy import select

from epic_events.controllers.roles_controller import create, delete
from epic_events.models.user import User


# A VERIFIER POURQUOI L'ID ??
def test_create_roles(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(create, ["-i", "1", '-n', 'support'],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
    })

    assert result.exit_code == 0
    assert "\n 'SUPPORT'created successfully.\n\n" in result.output


def test_delete_roles_not_found(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(delete, ["-i", "5"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
    })

    print('RESULTAT :', result.output)
    assert "\n Role with ID '5' is 'not found'.\n\n" in result.output
    assert result.exit_code == 0


"""
#Voir problème lien dans les tables user.role
def test_delete_roles(runner, mocked_session):
    user_logged = mocked_session.scalar(select(User).where(User.id == 2))
    result = runner.invoke(delete, ["-i", "3"],
                           obj={
                               "session": mocked_session,
                               "user_id": user_logged
                           })

    print('RESULTAT :', result.output)
    assert "\n Role with ID '3', 'COMMERCIAL' has been 'deleted'.\n" in result.output
    assert result.exit_code == 0
"""
