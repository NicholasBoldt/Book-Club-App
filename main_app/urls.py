from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # path('', views.home, name='home')
    path('', views.home, name='home'),
    path('clubs/', views.clubs_index, name='index'),
    path('clubs/<int:club_id>/', views.club, name='club'),
    path('clubs/<int:club_id>/selectbook/', views.select_book, name='selectbook'),
    path('clubs/<int:club_id>/recommendations/', views.recommendations, name='recommendations'),
    path('clubs/<int:club_id>/<int:meeting_id>/', views.meeting, name='meeting'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup')
]