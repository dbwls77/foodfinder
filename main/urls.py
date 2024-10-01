from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Ensure this is correct
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logged_out.html'), name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('favorites/', views.favorites, name='favorites'),
    path('search/', views.restaurant_search, name='restaurant-search'),
    path('restaurants/', views.restaurant_list, name='restaurant-list'),
    path('fetch-restaurants/', views.fetch_restaurants, name='fetch-restaurants'),
    path('map/', views.restaurant_map, name='restaurant-map'),
    path('add_favorite/<int:restaurant_id>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<int:restaurant_id>/', views.remove_favorite, name='remove_favorite'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
]
