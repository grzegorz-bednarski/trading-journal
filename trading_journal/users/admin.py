from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """
    Admin interface customization for the User model

    This class customizes the Django administration interface for the User model. It defines
    the layouts of forms for changing and adding User instances, specifies fields to include
    in each form, and configures the displayed columns, search fields, and ordering in the
    admin list view.

    Attributes:
        form: Form for changing existing User instances.
        add_form: Form for creating new User instances.
        fieldsets: Configuration for sections and fields to display in the forms for changing User instances.
        list_display: Fields to display in the User list view in the admin interface.
        search_fields: Fields to include in the search functionality in the User list view.
        ordering: Default ordering of User instances in the list view.
        add_fieldsets: Configuration for sections and fields to display in the form for adding new User instances.
    """

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
