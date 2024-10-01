# main/models.py
from django.db import models
from django.contrib.auth.models import User  # Import the User model

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=100)
    latitude = models.FloatField()  # For distance calculations
    longitude = models.FloatField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)  # Rating out of 5
    distance = models.FloatField()  # Distance from a reference point (optional for now)
    favorites = models.ManyToManyField(User, related_name='favorite_restaurants', blank=True)  # Reference User model

    def __str__(self):
        return self.name
