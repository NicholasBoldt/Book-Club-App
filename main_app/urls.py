from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.home, name='home')
    path('', views.home, name='home'),
    path('selectbook/', views.select_book, name='selectbook')
    path('clubs/', views.clubs_index, name='index'),
]