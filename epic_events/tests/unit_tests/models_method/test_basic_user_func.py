from unittest.mock import patch

import click
import passlib.hash

import pytest

from epic_events.models.user import User
from epic_events.controllers.user_controller import email_is_valid, change_password


def test_hash_pass_confirm_pass_valid():
    user = User()
    user_entry = "S3cret@23"
    initial_pass = "S3cret@23"
    hashed_initial_pass = passlib.hash.argon2.using(rounds=12).hash(initial_pass)
    user.password = hashed_initial_pass
    with patch('epic_events.models.user.input_old_pass', return_value=user_entry):
        checking = user.confirm_pass(user.password)
        assert checking is True


def test_wrong_hash_pass_confirm_pass_invalid():
    user = User()
    user_entry = "S3cret@2"
    initial_pass = "S3cret@23"
    hashed_initial_pass = passlib.hash.argon2.using(rounds=12).hash(initial_pass)
    user.password = hashed_initial_pass
    with patch('epic_events.models.user.input_old_pass', return_value=user_entry):
        checking = user.confirm_pass(user.password)
    assert checking is False


def test_email_is_valid(capsys):
    valid_email = "Jean.Pierre@epicevent.com"
    result = email_is_valid(None, None, valid_email)
    assert result == valid_email


def test_email_is_not_valid(capsys):
    invalid_email = "Jean.Pierreepicevent.com"
    with pytest.raises(click.UsageError):
        email_is_valid(None, None, invalid_email)

    capture = capsys.readouterr()
    assert "\nThe 'Email' you provided is 'invalid'\n" in capture.out


def test_change_password_wrong_entry(mock_specific_user, capsys):
    user = mock_specific_user[0]
    user_input = "wrong_pass"

    with patch('epic_events.models.user.input_old_pass', return_value=user_input):
        with pytest.raises(click.UsageError):
            with patch.object(User, 'confirm_pass', return_value=False):
                change_password(user, None)

    capture = capsys.readouterr()
    assert "\n' You enter a wrong password' \n\n" in capture.out


# Vérifier
def test_change_password_valid(mock_specific_user, capsys):
    user = mock_specific_user[0]
    user_old_pass = "S3cret@23"
    user_new_pass = "S3cret@24"
    with patch('epic_events.models.user.input_old_pass', return_value=user_old_pass):
        with patch('epic_events.controllers.user_controller.new_pass', return_value=user_new_pass):
            hash = user.hash_pass(user_new_pass)
            result = user.confirm_pass(hash)
            assert result is False


def test_change_password_confirm_wrong(mock_specific_user, capsys):
    user = mock_specific_user[0]
    user_old_pass = "S3cret@23"
    user_new_pass = "S3cret@24"
    with patch('epic_events.models.user.input_old_pass', return_value=user_old_pass):
        with patch('epic_events.controllers.user_controller.new_pass', return_value=user_new_pass):
            user.hash_pass(user_new_pass)
            with pytest.raises(click.UsageError):
                with patch.object(User, 'confirm_pass', return_value=False):
                    change_password(user, None)

        capture = capsys.readouterr()
        assert "\n' You enter a wrong password' \n\n" in capture.out
