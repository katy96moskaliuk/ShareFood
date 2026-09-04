from django.shortcuts import redirect, render
from .forms import FoodListingForm
from .models import FoodListing


def listings_list(request):
    if request.method == "POST":
        form = FoodListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")  # Перенаправление прямо на главную страницу
    else:
        form = FoodListingForm()

    listings = FoodListing.objects.all().order_by("-created_at")
    return render(
        request, "listings/index.html", {"listings": listings, "form": form}
    )