from django.shortcuts import redirect, render
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