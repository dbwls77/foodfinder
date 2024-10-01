from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, RestaurantSearchForm
from .models import Restaurant
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import json
from django.contrib.auth import authenticate, login



class CustomLoginView(LoginView):
    template_name = 'main/login.html'  # Specify your login template here
    # You can also define success_url if needed
    success_url = reverse_lazy('index')  # Redirect to index or another URL upon successful login

def get_success_url(self):
    return reverse_lazy('index')  # Redirect to the index view after successful login

@login_required
def index(request):
    return render(request, 'main/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the main page after login
        else:
            return render(request, 'main/login.html', {'error': 'Invalid credentials'})
    return render(request, 'main/login.html')  # Display the login form

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def favorites(request):
    user_favorites = request.user.favorite_restaurants.all() if request.user.is_authenticated else []
    return render(request, 'main/favorites.html', {'favorites': user_favorites})

@login_required
def add_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.favorites.add(request.user)
    return redirect('favorites')

@login_required
def remove_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.favorites.remove(request.user)
    return redirect('favorites')

@login_required
def restaurant_search(request):
    form = RestaurantSearchForm(request.GET or None)
    restaurants = Restaurant.objects.all()
    user_favorites = request.user.favorite_restaurants.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        cuisine_type = form.cleaned_data.get('cuisine_type')

        if name:
            restaurants = restaurants.filter(name__icontains=name)
        if cuisine_type:
            restaurants = restaurants.filter(cuisine_type__icontains=cuisine_type)

    restaurant_data = []
    for restaurant in restaurants:
        is_favorite = restaurant in user_favorites
        restaurant_data.append({'restaurant': restaurant, 'is_favorite': is_favorite})

    context = {
        'form': form,
        'restaurant_data': restaurant_data
    }

    return render(request, 'main/restaurant_search.html', context)

def fetch_restaurants(request):
    # This function would typically fetch restaurants from an external API or database.
    restaurants = Restaurant.objects.all()
    return render(request, 'main/restaurant_list.html', {'restaurants': restaurants})

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'main/restaurant_list.html', {'restaurants': restaurants})

def restaurant_map(request):
    restaurants = Restaurant.objects.all()

    # Convert Decimal fields to float for JSON serialization
    restaurant_data = []
    for restaurant in restaurants:
        restaurant_info = {
            "name": restaurant.name,
            "cuisine_type": restaurant.cuisine_type,
            "latitude": float(restaurant.latitude),  # Ensure latitude is a float
            "longitude": float(restaurant.longitude),  # Ensure longitude is a float
            # Add any other fields as necessary
        }
        restaurant_data.append(restaurant_info)

    # Serialize restaurant data to JSON
    restaurants_json = json.dumps(restaurant_data)

    return render(request, 'main/restaurant_map.html', {'restaurants': restaurants_json})
