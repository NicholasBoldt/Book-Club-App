from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.home, name='home')
    path('', views.home, name='home'),
    path('selectbook/', views.select_book, name='selectbook'),
    path('clubs/', views.clubs_index, name='index'),
    path('clubs/<int:pk>/update/', views.ClubUpdate.as_view(), name='clubs_update'),
    path('clubs/<int:pk>/delete/', views.ClubDelete.as_view(), name='clubs_delete'),
]