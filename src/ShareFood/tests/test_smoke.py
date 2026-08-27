import pytest


def test_smoke():
    assert 1 + 1 == 2


@pytest.mark.django_db
def test_database_access():
    from django.contrib.auth.models import User
    assert User.objects.count() == 0