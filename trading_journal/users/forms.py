from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    """
    UserAdminChangeForm is a custom form for changing User instances within the Django admin.

    Meta:
        Meta class that provides additional configuration for the form.

    Attributes:
        model: Specifies the model associated with this form.
        field_classes: Dictates the specific field classes to use for certain fields, in this case,
        an "EmailField" for the "email" field.
    """

    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """

    UserAdminCreationForm is a custom form for creating new users in the admin interface.
    It inherits from the UserCreationForm provided by admin_forms and customizes the fields and error messages.

    class Meta is an inner class that specifies the model and fields used by the form.

    model: Specifies that the form is associated with the User model.

    fields: Defines the fields to be used in the form, in this case, only the "email" field.

    field_classes: Specifies custom field classes for the form fields, here EmailField is used for the "email"
    field.

    error_messages: Customizes the error messages displayed for form validation errors. The "email" field has
    a unique constraint error message indicating that the email has already been taken.

    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }
