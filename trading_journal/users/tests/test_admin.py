from http import HTTPStatus

from django.urls import reverse

from trading_journal.users.models import User


class TestUserAdmin:
    """
    Test cases for the Django admin interface of the User model.

    This class provides tests for different actions that can be performed in the Django admin
    for User model, including viewing the changelist, adding users, searching users, and viewing a specific user.
    """

    def test_changelist(self, admin_client):
        """
        Test the User changelist view in the admin.

        This ensures that the changelist page for users is accessible to the admin client.
        """
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_search(self, admin_client):
        """
        Test the search functionality in the User changelist view.

        This ensures that the search works as expected and the admin client can perform a search.
        """
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == HTTPStatus.OK

    def test_add(self, admin_client):
        """
        Test adding a new user via the admin add view.

        This ensures that the add user form can be accessed, and a new user can be successfully created.
        """
        url = reverse("admin:users_user_add")
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK

        # Test the form submission to create a new user
        response = admin_client.post(
            url,
            data={
                "email": "new-admin@example.com",
                "password1": "My_R@ndom-P@ssw0rd",
                "password2": "My_R@ndom-P@ssw0rd",
            },
        )
        assert response.status_code == HTTPStatus.FOUND  # Expect redirect after successful add
        assert User.objects.filter(email="new-admin@example.com").exists()

    def test_view_user(self, admin_client):
        """
        Test viewing a specific user's detail page in the admin.

        This ensures that an admin client can access the change view for an existing user.
        """
        user = User.objects.get(email="admin@example.com")
        url = reverse("admin:users_user_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK
