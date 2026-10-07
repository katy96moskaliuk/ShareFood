from django.db import models
from django.conf import settings


class FoodListing(models.Model):
    CATEGORY_CHOICES = [
        ("fruits", "Fruits"),
        ("vegetables", "Vegetables"),
        ("grains", "Grains & Pasta"),
        ("canned", "Canned Food"),
        ("drinks", "Drinks"),
        ("sweets", "Sweets",),
        ("bakery", "Bread & Bakery"),
        
    ]

    DISTRICT_CHOICES = [
        ("centru", "Centru"),
        ("botanica", "Botanica"),
        ("buiucani", "Buiucani"),
        ("riscani", "Riscani"),
        ("ciocana", "Ciocana"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.CharField(max_length=100)
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    image = models.ImageField(upload_to="listings/")
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title