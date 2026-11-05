from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils import timezone

from .forms import FoodListingForm
from .models import FoodListing


def listings_list(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = FoodListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect("/")
    else:
        form = FoodListingForm()

    # Read filters from the query string and ignore unknown values
    district = request.GET.get("district", "")
    category = request.GET.get("category", "")
    show_expired = bool(request.GET.get("show_expired"))

    listings = FoodListing.objects.all().order_by("-created_at")  # pylint: disable=no-member

    if district in dict(FoodListing.DISTRICT_CHOICES):
        listings = listings.filter(district=district)
    else:
        district = ""

    if category in dict(FoodListing.CATEGORY_CHOICES):
        listings = listings.filter(category=category)
    else:
        category = ""

    # Hide expired listings unless explicitly requested
    if not show_expired:
        listings = listings.filter(expiration_date__gte=timezone.localdate())

    return render(request, "listings/index.html", {
        "listings": listings,
        "form": form,
        "districts": FoodListing.DISTRICT_CHOICES,
        "categories": FoodListing.CATEGORY_CHOICES,
        "current_district": district,
        "current_category": category,
        "show_expired": show_expired,
        "has_filters": bool(district or category or show_expired),
    })


@login_required
def my_listings(request):
    listings = FoodListing.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "listings/my_listings.html", {"listings": listings})


@login_required
@require_POST
def listing_delete(request, pk):
    listing = get_object_or_404(FoodListing, pk=pk, owner=request.user)
    listing.delete()
    return redirect("listings:my")


@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(FoodListing, pk=pk, owner=request.user)
    if request.method == "POST":
        form = FoodListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("listings:my")
    else:
        form = FoodListingForm(instance=listing)
    return render(
        request, "listings/listing_edit.html", {"form": form, "listing": listing}
    )


