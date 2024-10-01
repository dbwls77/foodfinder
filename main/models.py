from django.contrib.auth.models import User
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    cuisine_type = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    distance = models.FloatField()
    favorites = models.ManyToManyField(User, related_name='favorite_restaurants', blank=True)

    def __str__(self):
        return self.name
