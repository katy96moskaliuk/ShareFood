import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_register_creates_user(client):
    response = client.post(
        reverse("register"),
        {
            "username": "anna",
            "email": "anna@example.com",
            "password1": "StrongPass12345",
            "password2": "StrongPass12345",
        },
    )
    assert response.status_code == 302
    assert response.url == reverse("home")
    assert User.objects.filter(username="anna").exists()