from django.shortcuts import render, redirect
from .forms import FoodListingForm
from .models import FoodListing


def listings_list(request):
    if request.method == "POST":
        form = FoodListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listings_list")
    else:
        form = FoodListingForm()

    listings = FoodListing.objects.all().order_by("-created_at")
    return render(
        request,
        "listings/index.html",
        {"listings": listings, "form": form},
    )