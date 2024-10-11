from io import StringIO

import pytest
from django.core.management import call_command

from trading_journal.users.models import User


@pytest.mark.django_db
class TestUserManager:
    """
    Unit tests for the User model manager.

    These tests validate the behavior of the custom User model managers,
    specifically for creating regular users and superusers, as well as ensuring
    that certain attributes like username are handled appropriately.

    test_create_user
        Tests the creation of a regular user.
        Validates that the created user has the correct email, is not staff or
        superuser, checks the password, and confirms that the username is None.

    test_create_superuser
        Tests the creation of a superuser.
        Validates that the created superuser has the correct email, is staff,
        is a superuser, and confirms that the username is None.

    test_create_superuser_username_ignored
        Tests that when creating a superuser, the username is ignored and remains None.
    """

    def test_create_user(self):
        user = User.objects.create_user(
            email="john@example.com",
            password="something-r@nd0m!",  # noqa: S106
        )
        assert user.email == "john@example.com"
        assert not user.is_staff
        assert not user.is_superuser
        assert user.check_password("something-r@nd0m!")
        assert user.username is None

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="something-r@nd0m!",  # noqa: S106
        )
        assert user.email == "admin@example.com"
        assert user.is_staff
        assert user.is_superuser
        assert user.username is None

    def test_create_superuser_username_ignored(self):
        user = User.objects.create_superuser(
            email="test@example.com",
            password="something-r@nd0m!",  # noqa: S106
        )
        assert user.username is None


@pytest.mark.django_db
def test_createsuperuser_command():
    """
    Executes the Django 'createsuperuser' management command with specified email
    address, in a non-interactive mode, and verifies the superuser creation.

    :return: None
    """
    out = StringIO()
    command_result = call_command(
        "createsuperuser",
        "--email",
        "henry@example.com",
        interactive=False,
        stdout=out,
    )

    assert command_result is None
    assert out.getvalue() == "Superuser created successfully.\n"
    user = User.objects.get(email="henry@example.com")
    assert not user.has_usable_password()
