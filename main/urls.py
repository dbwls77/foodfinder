from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logged_out.html'), name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('favorites/', views.favorites, name='favorites'),
    path('search/', views.restaurant_search, name='restaurant-search'),
    path('restaurants/', views.restaurant_list, name='restaurant-list'),
    path('fetch-restaurants/', views.fetch_restaurants, name='fetch-restaurants'),
    path('map/', views.restaurant_map, name='restaurant-map'),
    path('search/', views.more_info, name='search'),  # New URL pattern
]

