# main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from .models import Restaurant

def index(request):
    return render(request, 'main/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def about(request):
    return render(request, 'main/about.html')

def map_view(request):
    restaurants = Restaurant.objects.all()  # Get all restaurant data
    return render(request, 'main/map.html', {'restaurants': restaurants})

def contact(request):
    return render(request, 'main/contact.html')

def favorites(request):
    return render(request, 'main/favorites.html') #Renders the favorites tab


