from django.shortcuts import render, redirect
from django.urls import reverse
import requests 
import os 
from .models import Book, Rec
from .models import Club, Meeting
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Book, Rec, User, Discussion
from .models import Club
from django.views.generic.edit import CreateView
from django.views.generic import ListView, CreateView, DetailView




# Create your views here.
def home(request):
    form = AuthenticationForm
    return render(request, 'landing.html', {'form': form})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    class form(UserCreationForm):
        class Meta:
            model = User
            fields = ('username', 'email', 'password1', 'password2')
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


    
def select_book(request, club_id):
    books = None
    if request.method == 'GET': # isbn search
        if 'isbn' in request.GET:
            isbn = [request.GET['isbn']]
            books = search_isbn(isbn)
        elif 'search_title' in request.GET: # author/title search
            books = search_title_author(request.GET['search_title'], request.GET['search_author'])
        return render(request, 'selectbook.html', { 'books' : books, 'club_id': club_id})
    elif request.method == 'POST': # add selected title to database
        # print('Title: ', request.POST['title'], "\n Author: ", request.POST['author'], "\n Description: ",request.POST['desc'], "\n ISBN: ", request.POST['isbn'], "\n Image: ", request.POST['image_link'])
        new_book = Book(
            title=request.POST['title'],
            author=request.POST['author'],
            desc=request.POST['desc'],
            isbn=request.POST['isbn'],
            image=request.POST['image_link'],
            club=Club.objects.get(id=club_id)
            )
        new_book.save()
        books = None
        club = Club.objects.get(id=club_id)
        rec_list = club.book_set.all()
        return redirect('/clubs/' + str(club_id) +'/recommendations')
    
    # return render(request, 'selectbook.html', { 'books' : books, 'club_id': club_id})

def search_isbn(isbn_list): # takes a list of ISBN numbers and returns a list of objects containing book, author, isbn, desc and image
    books = []
    my_key = os.environ['GOOGLE_BOOKS_API_KEY']
    for i, isbn in enumerate(isbn_list):
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(isbn) + '&printType=BOOKS&key=' + my_key).json()
        if r['totalItems'] == 0:
            books.append({ 'error' : 'Book not found. Please check your search and try again'})
        else:
            title = r['items'][0]['volumeInfo']['title']
            author = r['items'][0]['volumeInfo']['authors'][0]
            desc = r['items'][0]['volumeInfo']['description']
            if 'imageLinks' in r['items'][0]['volumeInfo']:
                image_link = r['items'][0]['volumeInfo']['imageLinks']['thumbnail']
            else:   
                image_link = None

            books.append({
                'title': title,
                'author': author,
                'image_link': image_link,
                'isbn' : isbn,
                'desc' : desc,
            })
    return books

def search_title_author(search_title, search_author): # searches title and author keywords to return a list of isbns, then uses search_isbn to return a list of objects containing book, author, isbn, desc, and image
    MAX = 5 #maximum titles to return
    isbn = []
    my_key = os.environ['GOOGLE_BOOKS_API_KEY']
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + search_title + '+inauthor:' + search_author +'&maxResults=' + str(MAX) + '&orderBy=relevance&printType=BOOKS&key=' + my_key).json()
    if r['totalItems'] < MAX:
        MAX = r['totalItems']
    for x in range(MAX):
        if 'industryIdentifiers' in r['items'][x]['volumeInfo']:
            num = r['items'][x]['volumeInfo']['industryIdentifiers'][0]['identifier']
            if num.isnumeric(): # filters out non-ISBN identifiers, which contain letter codes
                isbn.append(num)
    if len(isbn) == 0:
        isbn = [0]            

    books = search_isbn(isbn)
    return books

# Some test ISBNs:
# 9781609618957
# 9780140441185

# def add_comment(request, club_id, meeting_id)
#     return render(request, 'addcomment.html', meeting_id)

def add_comment(request, club_id, meeting_id):
    user = request.user.id
    if request.method == 'GET':
        return render(request, 'addcomment.html', {'user':user, 'meeting' : meeting_id})
    elif request.method == 'POST':
        print('User id: ', user, "type:", type(user))
        new_comment = Discussion(
            disc_type = request.POST['disc_type'],
            user = User.objects.get(id=user),
            meeting = Meeting.objects.get(id=request.POST['meeting']),
            comment = request.POST['comment'],
        )
        new_comment.save()
        return redirect('/clubs/' + str(club_id) + '/meeting/' + str(meeting_id) + '/discussion')

class DiscussionList(ListView):
    model = Discussion

class RecList(ListView):
    model = Book

class UserProfile(DetailView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']

def clubs_index(request):
    clubs = Club.objects.all()
    print(clubs.__dict__)
    return render(request, 'myclubs/index.html', { 'clubs': clubs })

def club(request, club_id):
    club = Club.objects.get(id=club_id)
    return render(request, 'myclubs/club.html', { 'club': club})

def meeting(request, club_id, meeting_id):
    club = Club.objects.get(id=club_id)
    meeting = Meeting.objects.get(id=meeting_id)
    book = meeting.book
    return render(request, 'myclubs/meeting.html', { 'club': club, 'meeting': meeting, 'book': book})

class MeetingCreate(CreateView):
  model = Meeting
  fields = '__all__'
  success_url = 'clubs/<int:club_id>/meeting/<int:meeting_id>/create/'

class ClubCreate(CreateView):
  model = Club
  fields = '__all__'
  success_url = '/clubs/'

