from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path("", views.listings_list, name="list"),
    path("my/", views.my_listings, name="my"),
    path("<int:pk>/delete/", views.listing_delete, name="delete"),
    path("<int:pk>/edit/", views.listing_edit, name="edit"),
]
