from django.shortcuts import render, redirect
from .models import Club

# Create your views here.
def home(request):
    print("Working")

def clubs_index(request):
  clubs = Club.objects.all()
  return render(request, 'myclubs/index.html', { 'clubs': clubs })
