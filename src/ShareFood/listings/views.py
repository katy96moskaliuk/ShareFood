from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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

    listings = FoodListing.objects.all().order_by("-created_at")  # pylint: disable=no-member
    return render(
        request, "listings/index.html", {"listings": listings, "form": form}
    )


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