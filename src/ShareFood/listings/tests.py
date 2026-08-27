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
    url = reverse("listings_list")
    response = client.get(url)
    assert response.status_code == 200