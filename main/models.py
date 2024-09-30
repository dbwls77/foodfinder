# main/models.py
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=100)
    latitude = models.FloatField()  # For distance calculations
    longitude = models.FloatField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)  # Rating out of 5
    distance = models.FloatField()  # Distance from a reference point (optional for now)

    def __str__(self):
        return self.name
