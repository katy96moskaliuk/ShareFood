from django.db import models


class FoodListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title