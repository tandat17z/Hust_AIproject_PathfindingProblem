import re
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='map'),
    path('_<str:searchText>/', views.searchView, name='map'),
]
