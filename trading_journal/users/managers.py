from typing import TYPE_CHECKING

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager

if TYPE_CHECKING:
    from .models import User  # noqa: F401


class UserManager(DjangoUserManager["User"]):
    """
    UserManager is a custom user model manager that handles the creation
    of user and superuser accounts.

    Methods:
        _create_user(email, password, **extra_fields):
            Create and save a user with the given email and password.

        create_user(email, password=None, **extra_fields):
            Public method to create and save a standard user with the given
            email and password.

        create_superuser(email, password=None, **extra_fields):
            Public method to create and save a superuser with the given
            email and password.
    """

    def _create_user(self, email: str, password: str | None, **extra_fields):
        """
        :param email: User's email address, must be a valid email format and is required.
        :param password: User's password, can be None if the password is not required.
        :param extra_fields: Additional fields for creating the user, provided as keyword arguments.
        :return: The newly created user instance.
        """
        if not email:
            msg = "The given email must be set"
            raise ValueError(msg)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):  # type: ignore[override]
        """
        :param email:
        :param password:
        :param extra_fields:
        :return:

        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):  # type: ignore[override]
        """
        :param email: The email address for the superuser.
        :param password: The password for the superuser. If None, a password must be set later.
        :param extra_fields: Additional fields for the user model.
        :return: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(email, password, **extra_fields)
