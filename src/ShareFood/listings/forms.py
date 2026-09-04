from django import forms
from .models import FoodListing


class FoodListingForm(forms.ModelForm):
    class Meta:
        model = FoodListing
        fields = [
            "title",
            "description",
            "quantity",
            "district",
            "category",
            "expiration_date",
            "image",
        ]
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
        }