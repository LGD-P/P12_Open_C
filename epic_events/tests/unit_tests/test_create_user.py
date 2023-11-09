from epic_events.controllers import app
from epic_events.models.user import  User


def test_user_creation(runner, session_mock, check_auth_mock):

    result = runner.invoke(app, ["user", "create", "-n", "John Doe",
                                 "--email", "johndoe@example.com",
                                 "--role", "management", "--password",
                                 "S3@cret23"])

    assert result.exit_code == 0
    assert "\n 'JOHN DOE' created successfully.\n\n" in result.output

    # session_mock.add.assert_called_with(
      #  User(name='John Doe', email="john.doe@example.com", role='management', password='S3@cret23'))