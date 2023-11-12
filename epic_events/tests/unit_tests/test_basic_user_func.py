from unittest.mock import patch

import passlib.hash

from epic_events.models.user import User


def test_confirm_pass_valid():
    user = User()
    user_entry = "S3cret@23"
    initial_pass = "S3cret@23"
    hashed_initial_pass = passlib.hash.argon2.using(rounds=12).hash(initial_pass)
    user.password = hashed_initial_pass
    with patch('epic_events.models.user.input_old_pass', return_value=user_entry):
        checking = user.confirm_pass(user.password)
        assert checking


def test_wrong_confirm_pass_invalid():
    user = User()
    user_entry = "S3cret@2"
    initial_pass = "S3cret@23"
    hashed_initial_pass = passlib.hash.argon2.using(rounds=12).hash(initial_pass)
    user.password = hashed_initial_pass
    with patch('epic_events.models.user.input_old_pass', return_value=user_entry):
        checking = user.confirm_pass(user.password)
    assert not checking
