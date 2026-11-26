from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class FoodListing(models.Model):
    CATEGORY_CHOICES = [
        ("fruits", _("Fruits")),
        ("vegetables", _("Vegetables")),
        ("grains", _("Grains & Pasta")),
        ("canned", _("Canned Food")),
        ("drinks", _("Drinks")),
        ("sweets", _("Sweets")),
        ("bakery", _("Bread & Bakery")),
    ]

    DISTRICT_CHOICES = [
        ("centru", _("Centru")),
        ("botanica", _("Botanica")),
        ("buiucani", _("Buiucani")),
        ("riscani", _("Riscani")),
        ("ciocana", _("Ciocana")),
    ]

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    quantity = models.CharField(_("quantity"), max_length=100)
    district = models.CharField(_("district"), max_length=50, choices=DISTRICT_CHOICES)
    category = models.CharField(_("category"), max_length=50, choices=CATEGORY_CHOICES)
    expiration_date = models.DateField(_("best before"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    image = models.ImageField(_("photo"), upload_to="listings/")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
        null=True,
        blank=True,
        verbose_name=_("owner"),
    )

    class Meta:
        verbose_name = _("food listing")
        verbose_name_plural = _("food listings")

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        """True if the best-before date is already in the past."""
        return self.expiration_date < timezone.localdate()
