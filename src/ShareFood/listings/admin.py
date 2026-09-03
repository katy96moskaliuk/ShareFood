from django.contrib import admin
from .models import FoodListing


@admin.register(FoodListing)
class FoodListingAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "district", "expiration_date")
    list_filter = ("category", "district")
