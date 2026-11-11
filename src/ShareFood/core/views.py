from django.shortcuts import render
from django.utils import timezone

from listings.models import FoodListing


def home(request):
    # Only count listings that are not expired yet
    active = FoodListing.objects.filter(expiration_date__gte=timezone.localdate())

    stats = {
        "listings": active.count(),
        "districts": active.values("district").distinct().count(),
        "categories": active.values("category").distinct().count(),
    }
    return render(request, "core/index.html", {"stats": stats})