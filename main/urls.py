from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import views from the same app

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logged_out.html'), name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('favorites/', views.favorites, name='favorites'),
    path('search/', views.restaurant_search, name='restaurant-search'),  # Correct path for restaurant search
    path('restaurants/', views.restaurant_list, name='restaurant-list'),
    path('fetch-restaurants/', views.fetch_restaurants, name='fetch-restaurants'),
    path('map/', views.restaurant_map, name='restaurant-map'),
    path('add_favorite/<int:restaurant_id>/', views.add_favorite, name='add_favorite'),  # Add this line
    path('remove_favorite/<int:restaurant_id>/', views.remove_favorite, name='remove_favorite'),  # Add this line
]
