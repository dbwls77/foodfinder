import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, RestaurantSearchForm
from .models import Restaurant
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import json
from django.contrib.auth import authenticate, login

def get_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points using the Haversine formula."""
    R = 3958.8  # Radius of the Earth in miles

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    distance = R * c  # Distance in miles
    return distance

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

def restaurant_search(request):
    form = RestaurantSearchForm(request.GET or None)
    restaurants = Restaurant.objects.all().distinct()

    # Get user's latitude and longitude from the request if available
    user_latitude = request.GET.get('latitude', None)
    user_longitude = request.GET.get('longitude', None)

    if user_latitude is not None and user_longitude is not None:
        try:
            user_latitude = float(user_latitude)
            user_longitude = float(user_longitude)
        except ValueError:
            user_latitude = None
            user_longitude = None

    if form.is_valid():
        name = form.cleaned_data.get('name')
        cuisine_type = form.cleaned_data.get('cuisine_type')

        if name:
            restaurants = restaurants.filter(name__icontains=name)
        if cuisine_type:
            restaurants = restaurants.filter(cuisine_type__icontains=cuisine_type)

    restaurant_data = []
    for restaurant in restaurants:
        distance = None
        if user_latitude is not None and user_longitude is not None:
            if restaurant.latitude is not None and restaurant.longitude is not None:
                distance = get_distance(
                    user_latitude,
                    user_longitude,
                    float(restaurant.latitude),
                    float(restaurant.longitude)
                )

        restaurant_data.append({
            'restaurant': restaurant,
            'distance': distance,
        })

    # Optional: Sort restaurants by distance if distance is available
    restaurant_data_with_distance = [data for data in restaurant_data if data['distance'] is not None]
    restaurant_data_without_distance = [data for data in restaurant_data if data['distance'] is None]
    restaurant_data_with_distance.sort(key=lambda x: x['distance'])
    restaurant_data = restaurant_data_with_distance + restaurant_data_without_distance

    context = {
        'form': form,
        'restaurant_data': restaurant_data,
    }

    return render(request, 'main/restaurant_search.html', context)


def fetch_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'main/restaurant_list.html', {'restaurants': restaurants})

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'main/restaurant_list.html', {'restaurants': restaurants})

# main/views.py
from django.shortcuts import render
from .models import Restaurant
def restaurant_list(request):
    query = request.GET.get('q', '')  # Search term
    cuisine = request.GET.get('cuisine', '')  # Cuisine filter
    min_rating = request.GET.get('min_rating', 0)  # Minimum rating filter
    # Filter restaurants based on the query parameters
    restaurants = Restaurant.objects.all()
    if query:
        restaurants = restaurants.filter(name__icontains=query)
    if cuisine:
        restaurants = restaurants.filter(cuisine_type__icontains=cuisine)
    if min_rating:
        restaurants = restaurants.filter(rating__gte=min_rating)
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
