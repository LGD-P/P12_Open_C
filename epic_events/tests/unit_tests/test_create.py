from sqlalchemy import select

from epic_events.controllers import app
from epic_events.models.user import  User
from epic_events.models.role import  Role


def test_user_creation(runner,has_perm_mock,user_mock,session_mock, check_auth_mock, role_list_mock):
    """
    permission = ["support"]
    user_logged = user_mock[0]

    check_auth_mock(user_logged)
    print(user_logged.role.name)

    user_has_perm = has_perm_mock(permission, user_logged)

    assert user_has_perm is not None
    """

    result = runner.invoke(app, ["user", "create", "--name", "John Doe",
                                 "--email", "johndoe@example.com",
                                 "--role", "management", "--password",
                                 "S3@cret23"])

    role_to_fill = role_list_mock[0]

    password = User().hash_pass('S3cret@23')
    print("PASSWORD : ",password)

    new_user = User(id=1,name="John Doe", email="johndoe@example.com",
                    role=role_to_fill, password=password)
    print("USERNAME ",new_user.name)

    role_to_fill.users.append(new_user)
    print("ROLE TO FILL NAME",role_to_fill.name)

    print(session_mock.scalars(select(User).where(User.name == new_user.name)).return_value)
    print("USERNAME :",new_user.name)

    assert result.exit_code == 0
    assert "\n 'JOHN DOE' created successfully.\n\n" in result.output
    assert role_to_fill.users[1] == new_user



