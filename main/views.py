# main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm
from .models import Restaurant
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant  # Adjust this import if your models.py is in a different app


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
    return render(request, 'main/favorites.html')

@login_required
def add_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.favorites.add(request.user)
    return redirect('restaurant_search')  # Redirect to the restaurant search page

@login_required
def remove_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.favorites.remove(request.user)
    return redirect('restaurant_search')  # Redirect to the restaurant search page




from .models import Restaurant
from .forms import RestaurantSearchForm

# views.py
from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantSearchForm

# main/views.py
from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantSearchForm  # Assuming you have a form for searching

def restaurant_search(request):
    form = RestaurantSearchForm(request.GET or None)
    restaurants = Restaurant.objects.all()

    if form.is_valid():
        # Apply filtering based on the form inputs (e.g., name, cuisine_type)
        name = form.cleaned_data.get('name')
        cuisine_type = form.cleaned_data.get('cuisine_type')

        if name:
            restaurants = restaurants.filter(name__icontains=name)
        if cuisine_type:
            restaurants = restaurants.filter(cuisine_type__icontains=cuisine_type)

    context = {
        'form': form,
        'restaurants': restaurants
    }

    return render(request, 'restaurant_search.html', context)


# main/views.py
import requests
from django.http import HttpResponse
from .models import Restaurant

import requests
from django.http import HttpResponse
from .models import Restaurant

import requests
from django.http import HttpResponse
from .models import Restaurant

import requests
from django.http import HttpResponse
from .models import Restaurant

def fetch_restaurants(request):
    api_key = 'AIzaSyAlkqLV5Szqua_fdhTXBSJ-QJfAmukjQac'
    location = '33.7490,-84.3880'  # Example: Atlanta, GA
    radius = 20000  # Search within 2,000 meters

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type=restaurant&key={api_key}"
    response = requests.get(url)
    results = response.json().get('results', [])

    for place in results:
        name = place['name']
        latitude = place['geometry']['location']['lat']
        longitude = place['geometry']['location']['lng']
        rating = place.get('rating', 0)
        place_id = place['place_id']  # Get the place ID for more details

        # Make a request to the Place Details API to get more details
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
        details_response = requests.get(details_url)
        details_result = details_response.json().get('result', {})

        # Get types and infer cuisine type
        types = details_result.get('types', [])
        cuisine_type = infer_cuisine_type(types)

        # Save the restaurant to the database
        Restaurant.objects.create(
            name=name,
            cuisine_type=cuisine_type,
            latitude=latitude,
            longitude=longitude,
            rating=rating,
            distance=10  # You can calculate the distance if necessary
        )

    return HttpResponse(f"Added {len(results)} restaurants to the database.")

def infer_cuisine_type(types):
    if 'italian_restaurant' in types:
        return 'Italian'
    elif 'chinese_restaurant' in types:
        return 'Chinese'
    elif 'indian_restaurant' in types:
        return 'Indian'
    elif 'japanese_restaurant' in types:
        return 'Japanese'
    elif 'mexican_restaurant' in types:
        return 'Mexican'
    elif 'french_restaurant' in types:
        return 'French'
    else:
        return 'Unknown'  # Default if no specific cuisine type is found


# Function to save restaurant data into the database
def save_restaurants(results):
    for place in results:
        name = place['name']
        latitude = place['geometry']['location']['lat']
        longitude = place['geometry']['location']['lng']
        rating = place.get('rating', 0)
        cuisine_type = 'Unknown'  # Placeholder
        distance = 0  # Set default distance

        # Save the restaurant data into the database
        Restaurant.objects.create(
            name=name,
            cuisine_type=cuisine_type,
            latitude=latitude,
            longitude=longitude,
            rating=rating,
            distance=distance  # Ensure the distance field is set
        )


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

def more_info(request):
    print("More Info View Triggered")
    return render(request, 'main/more_info.html')  # Make sure you create a corresponding HTML file

def test_links(request):
    return render(request, 'main/test_links.html')

# main/views.py
from django.shortcuts import render
from .models import Restaurant

# main/views.py
from django.shortcuts import render
from .models import Restaurant
import json

def restaurant_map(request):
    # Fetch all restaurants from the database
    restaurants = Restaurant.objects.all()

    # Serialize the data into a JSON format
    restaurants_data = []
    for restaurant in restaurants:
        restaurants_data.append({
            'name': restaurant.name,
            'latitude': restaurant.latitude,
            'longitude': restaurant.longitude,
            'rating': float(restaurant.rating),  # Convert to float if it's a DecimalField
            'cuisine_type': restaurant.cuisine_type
        })

    # Pass the serialized data as JSON to the template
    context = {
        'restaurants': json.dumps(restaurants_data)  # Serialize data as JSON
    }

    return render(request, 'main/restaurant_map.html', context)

