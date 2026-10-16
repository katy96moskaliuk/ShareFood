from datetime import date
import pytest
from listings.models import FoodListing
from django.urls import reverse


@pytest.mark.django_db
def test_create_food_listing():
    listing = FoodListing.objects.create(
        title="Fresh Apples",
        description="Fresh apples from the garden, around 3 kg",
        quantity="3 kg",
        district="Centru",
        category="fruits",
        expiration_date=date(2026, 9, 1),
    )
    assert listing.title == "Fresh Apples"
    assert listing.category == "fruits"
    assert FoodListing.objects.count() == 1


@pytest.mark.django_db
def test_listings_list_view(client):
    url = reverse("listings:list")
    response = client.get(url)
    assert response.status_code == 200

    
@pytest.mark.django_db
def test_guest_cannot_create_listing(client):
    response = client.post(reverse("listings:list"), {"title": "Apples"})
    assert response.status_code == 302
    assert response.url == reverse("login")
    assert FoodListing.objects.count() == 0

@pytest.mark.django_db
def test_guest_cannot_open_my_listings(client):
    response = client.get(reverse("listings:my"))
    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


@pytest.mark.django_db
def test_my_listings_shows_only_own(client, django_user_model):
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    boris = django_user_model.objects.create_user(username="boris", password="StrongPass12345")
    FoodListing.objects.create(
        title="Annas apples", description="d", quantity="1 kg",
        district="centru", category="fruits",
        expiration_date=date(2026, 12, 1), owner=anna,
    )
    FoodListing.objects.create(
        title="Borises bread", description="d", quantity="1 pc",
        district="centru", category="bakery",
        expiration_date=date(2026, 12, 1), owner=boris,
    )
    client.force_login(anna)
    response = client.get(reverse("listings:my"))
    content = response.content.decode()
    assert "Annas apples" in content
    assert "Borises bread" not in content