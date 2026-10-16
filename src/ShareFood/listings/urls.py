from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path("", views.listings_list, name="list"),
    path("my/", views.my_listings, name="my"),
]