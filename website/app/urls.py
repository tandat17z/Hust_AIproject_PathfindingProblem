import re
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapView, name='map'),
    path('_<str:searchText>/', views.searchView, name='map'),
]
