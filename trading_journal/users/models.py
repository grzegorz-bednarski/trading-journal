from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Class User

        Custom user model overriding the default Django AbstractUser.
        Implements a user model using email instead of username.

        Attributes:
            name (CharField): User's full name. This field is optional.
            email (EmailField): User's email address. This is a unique and required field.
            username: Disabled username field inherited from AbstractUser.

        Constants:
            USERNAME_FIELD (str): Field for authentication. Set to use the email field.
            REQUIRED_FIELDS (list): List of fields required to create a superuser. Empty by default.

        Manager:
            objects (UserManager): The manager to manage the User objects.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()
