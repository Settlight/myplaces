from django.urls import path
from . import views

app_name = 'places'

urlpatterns = [
    path('', views.index, name='index'),
    path('places/', views.places_list, name='places_list'),
    path('places/add/', views.add_place, name='add_place'),
    path('places/pick/', views.pick_place, name='pick_place'),
    path('places/<str:place_id>/', views.place_detail, name='place_detail'),
]
