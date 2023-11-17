import pytest
from click.testing import CliRunner

from epic_events.models.base import Base
from epic_events.tests.fake_datas import (generate_user,
                                          generate_roles)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    return [("roles", [
                 {"id": 1,
                  "name": "support",
                  },
                 {"id": 2,
                  "name": "management",
                  },
                 {"id": 3,
                  "name": "commercial",
                  },
             ]),
            ("users", [
                {
                    "id": 1,
                    "name": "Kevin",
                    'email': "keven@epicevent.com",
                    'role_id': 1,
                    'password': "$argon2id$v=19$m=65536,t=12,"
                                "p=4$U8q5916rdY4xRgihdA4hZA$DG/JgT0jwh4ArcbMPQ7Xv3ZdOjUitPDn9KFq2jnbYH0"
                    # S3CRET@23
                },
                {
                    "id": 2,
                    "name": "Dwight",
                    'email': "Dwight@epicevent.com",
                    'role_id': 2,
                    'password': "$argon2id$v=19$m=65536,t=12,"
                                "p=4$ujdmTAmhVIoRglDKGWPMGQ$EuA/DgPVl95jk/OmNbYRfXRtLhao0d35ZjPSwHHhIeU"
                    # S3CRET@24
                },
                {
                    "id": 3,
                    "name": "Pierre",
                    'email': "Pierre@epicevent.com",
                    'role_id': 3,
                    'password': "$argon2id$v=19$m=65536,t=12,"
                                "p=4$eC+F8B5j7L2Xcu49B8D4Xw$WJQ7xOedcIUVk+U1W1xrWgzAUcLi33wbqKoC8m8cgzg"
                    # S3CRET@25
                }
            ]),
            ("clients",[] ),
            ("contracts", []),
            ("events", []),

            ]


@pytest.fixture
def role_list_mock():
    roles_list = generate_roles()
    return roles_list

@pytest.fixture
def mock_specific_user(role_list_mock):
    user_manager = generate_user(role_list_mock[0],1)
    user_commercial = generate_user(role_list_mock[1],2)
    user_support = generate_user(role_list_mock[2],3)
    users_list = [user_manager, user_commercial,user_support]
    return users_list











"""

@pytest.fixture()
def session_mock(mocker):
    session = MagicMock()
    session_class = MagicMock(return_value=session)
    mocker.patch('epic_events.database.sessionmaker',
                 return_value=session_class)
    return session




    
@pytest.fixture
def user_mock(role_list_mock):
    user_manager = generate_user(role_list_mock[0], 1)
    user_commercial = generate_user(role_list_mock[1], 2)
    user_support = generate_user(role_list_mock[2], 3)
    users_list = [user_manager, user_commercial, user_support]
    return users_list









@pytest.fixture
def check_auth_mock(mocker, user_mock):
    def create_choice(user_number):
        def check_auth(func):
            def wrapper(ctx, *args, **kwargs):
                ctx.obj["user_id"] = user_mock[user_number]
                return func(ctx, *args, **kwargs)

            return wrapper

        mocker.patch("epic_events.utils.check_authentication",
                     return_value=check_auth)

    return create_choice


@pytest.fixture
def has_perm_mock(mocker):
    def create_mock(allowed_roles, user):
        def check_perm(func):
            def wrapper(ctx, *args, **kwargs):
                ctx.obj["user_id"].role_id = user.role_id
                if user.role.name not in allowed_roles:
                    return print("\n'You're not allowed to use this command'\n")

                return func(ctx, *args, **kwargs)

            return wrapper

        return mocker.patch("epic_events.utils.has_permission", wraps=check_perm)

    return create_mock








'''
@pytest.fixture
def has_perm_mock(mocker):
    def create_mock(permission, user_mock):
        return mocker.patch(
            "epic_events.utils.has_permission",
            return_value=f"\n'You're not allowed to use this command'\n"
        ) if user_mock.role.name not in permission else None
    return create_mock
'''



"""
