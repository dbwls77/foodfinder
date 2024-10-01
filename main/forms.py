# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RestaurantSearchForm(forms.Form):
    name = forms.CharField(required=False, label='Restaurant Name', max_length=100)
    cuisine_type = forms.CharField(required=False, label='Cuisine Type', max_length=100)
    rating = forms.DecimalField(required=False, min_value=0, max_value=5, label='Minimum Rating')
    max_distance = forms.FloatField(required=False, label='Maximum Distance')
