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
        district="centru",
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


def make_listing(owner, title="Apples"):
    return FoodListing.objects.create(
        title=title,
        description="d",
        quantity="1 kg",
        district="centru",
        category="fruits",
        expiration_date=date(2026, 12, 1),
        owner=owner,
    )


@pytest.mark.django_db
def test_owner_can_delete_listing(client, django_user_model):
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    listing = make_listing(anna)
    client.force_login(anna)
    response = client.post(reverse("listings:delete", args=[listing.pk]))
    assert response.status_code == 302
    assert FoodListing.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_delete_foreign_listing(client, django_user_model):
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    boris = django_user_model.objects.create_user(username="boris", password="StrongPass12345")
    listing = make_listing(anna)
    client.force_login(boris)
    response = client.post(reverse("listings:delete", args=[listing.pk]))
    assert response.status_code == 404
    assert FoodListing.objects.count() == 1


@pytest.mark.django_db
def test_guest_cannot_delete_listing(client, django_user_model):
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    listing = make_listing(anna)
    response = client.post(reverse("listings:delete", args=[listing.pk]))
    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))
    assert FoodListing.objects.count() == 1


@pytest.mark.django_db
def test_delete_requires_post(client, django_user_model):
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    listing = make_listing(anna)
    client.force_login(anna)
    response = client.get(reverse("listings:delete", args=[listing.pk]))
    assert response.status_code == 405
    assert FoodListing.objects.count() == 1

@pytest.mark.django_db
def test_owner_can_open_edit_page(client, django_user_model):
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    listing = make_listing(anna)
    client.force_login(anna)
    response = client.get(reverse("listings:edit", args=[listing.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_cannot_open_foreign_edit_page(client, django_user_model):
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    boris = django_user_model.objects.create_user(username="boris", password="StrongPass12345")
    listing = make_listing(anna)
    client.force_login(boris)
    response = client.get(reverse("listings:edit", args=[listing.pk]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_guest_cannot_open_edit_page(client, django_user_model):
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    listing = make_listing(anna)
    response = client.get(reverse("listings:edit", args=[listing.pk]))
    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


# ---------- Redirects keep the language prefix (/uk/, /ru/, ...) ----------

# Smallest valid GIF (1x1 px) so the required image field passes validation
TINY_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04"
    b"\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


@pytest.mark.django_db
def test_create_listing_redirect_keeps_language(client, django_user_model, settings, tmp_path):
    from django.core.files.uploadedfile import SimpleUploadedFile

    settings.MEDIA_ROOT = tmp_path
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    client.force_login(anna)
    response = client.post("/uk/listings/", {
        "title": "Apples",
        "description": "d",
        "quantity": "1 kg",
        "district": "centru",
        "category": "fruits",
        "expiration_date": "2026-12-31",
        "image": SimpleUploadedFile("apple.gif", TINY_GIF, content_type="image/gif"),
    })
    assert response.status_code == 302
    assert response.url == "/uk/"
    assert FoodListing.objects.count() == 1


@pytest.mark.django_db
def test_guest_post_redirects_to_login_in_same_language(client):
    response = client.post("/ro/listings/", {"title": "Apples"})
    assert response.status_code == 302
    assert response.url == "/ro/accounts/login/"


@pytest.mark.django_db
def test_delete_redirect_keeps_language(client, django_user_model):
    anna = django_user_model.objects.create_user(username="anna", password="StrongPass12345")
    listing = make_listing(anna)
    client.force_login(anna)
    response = client.post(f"/ru/listings/{listing.pk}/delete/")
    assert response.status_code == 302
    assert response.url.startswith("/ru/")
