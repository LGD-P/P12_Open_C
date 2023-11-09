import pytest
from unittest.mock import MagicMock
from click.testing import CliRunner
from epic_events.tests.fake_datas import generate_user


@pytest.fixture
def session_mock(mocker):
    session = MagicMock()
    session_class = MagicMock(return_value=session)
    mocker.patch('epic_events.database.create_engine')
    mocker.patch('epic_events.database.sessionmaker',
                 return_value=session_class)
    return session


@pytest.fixture
def user_mock(mocker):
    user = generate_user('Pierre Henri', 'management')
    return user


@pytest.fixture
def check_auth_mock(mocker, user_mock):
    def check_auth(func):
        def wrapper(ctx, *args, **kwargs):
            ctx.obj["user_id"] = user_mock
            return func(ctx, *args, **kwargs)
        return wrapper

    mocker.patch("epic_events.utils.check_authentication",
                 return_value=check_auth)


@pytest.fixture
def runner():
    return CliRunner()
