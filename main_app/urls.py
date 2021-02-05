from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('invitecode/', views.enter_code),
    path('invitecode/<str:invite_code>/', views.invite_lookup, name='invitelookup'),
    path('clubs/', views.clubs_index, name='index'),
    path('clubs/<int:club_id>/meeting', views.club, name='club'),
    path('clubs/<int:club_id>/join', views.join_club, name='joinclub'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/selectbook/', views.select_book, name='selectbook'),
    path('clubs/<int:pk>/recommendations/', views.RecList.as_view(), name='recommendations'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/recommendations/', views.add_from_list, name='addrecc'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/', views.meeting, name='meeting'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/rate/', views.rate, name='rate'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/discussion/', views.discussion_list, name='discussion'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/discussion/add/', views.add_comment, name='addcomment'),
    path('clubs/<int:club_id>/meeting/<int:meeting_id>/discussion/delete/', views.delete_comment, name='deletecomment'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/user/<int:pk>/', views.UserProfile.as_view(), name='userprofile'),
    path('clubs/create/', views.create_club, name='clubs_create'),
    path('clubs/<int:club_id>/meeting/<int:pk>/update/', views.MeetingUpdate.as_view(), name='meeting_update'),
    
    


]