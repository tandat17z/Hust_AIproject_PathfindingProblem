import re
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='choose'),
    path('_<str:searchText>/', views.searchView, name='finding'),
]
