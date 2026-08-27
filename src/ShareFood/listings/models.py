from django.db import models


class FoodListing(models.Model):
    CATEGORY_CHOICES = [
        ("fruits", "Fruits"),
        ("vegetables", "Vegetables"),
        ("grains", "Grains & Pasta"),
        ("canned", "Canned Food"),
        ("drinks", "Drinks"),
        ("sweets", "Sweets"),
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

    def __str__(self):
        return self.title