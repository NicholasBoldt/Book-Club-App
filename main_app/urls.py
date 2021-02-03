from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('clubs/', views.clubs_index, name='index'),
    path('clubs/<int:club_id>/', views.club, name='club'),
    path('clubs/<int:club_id>/selectbook/', views.select_book, name='selectbook'),
    path('clubs/<int:pk>/recommendations/', views.RecList.as_view(), name='recommendations'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/', views.meeting, name='meeting'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/discussion/', views.DiscussionList.as_view(), name='discussion'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/discussion/add/', views.add_comment, name='addcomment'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/user/<int:pk>/', views.UserProfile.as_view(), name='userprofile'),
    path('clubs/create/', views.ClubCreate.as_view(), name='clubs_create'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/create/', views.ClubCreate.as_view(), name='meetings_create'),


]