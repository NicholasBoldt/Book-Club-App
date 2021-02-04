from django.shortcuts import render, redirect
from django.urls import reverse
import requests 
import os 
from .models import Book, User, Discussion, Rating, Club, Meeting
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
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


@login_required    
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

@login_required
def add_comment(request, club_id, meeting_id):
    user = request.user.id
    if request.method == 'GET':
        return render(request, 'addcomment.html', {'user':user, 'meeting' : meeting_id})
    elif request.method == 'POST':
        new_comment = Discussion(
            disc_type = request.POST['disc_type'],
            user = User.objects.get(id=user),
            meeting = Meeting.objects.get(id=request.POST['meeting']),
            comment = request.POST['comment'],
        )
        new_comment.save()
        return redirect('/clubs/' + str(club_id) + '/meeting/' + str(meeting_id) + '/discussion', {'club_id':club_id, 'meeting_id':meeting_id})

@login_required
def enter_code(request):
    return redirect('/invitecode/' + request.POST['invite_code'])

def invite_lookup(request, invite_code):
    club = Club.objects.get(invite=invite_code)
    print(invite_code, club.id)
    meeting = Meeting.objects.all().filter(club_id=club.id)
    recent = meeting.last()
    print(recent)
    return render(request, 'invitelookup.html', {'club':club, 'book': recent.book})

@login_required
def join_club(request, club_id):
    club = Club.objects.get(id=club_id)
    club.members.add(User.objects.get(id=request.user.id))
    return redirect('index')

@login_required
def delete_comment(request, club_id, meeting_id):
    comment = Discussion.objects.get(id=request.POST['commentid'])
    comment.delete()
    return redirect('/clubs/' + str(club_id) + '/meeting/' + str(meeting_id) + '/discussion')


class DiscussionList(ListView):
    model = Discussion

    def get_context_data(self, **kwargs):
        meeting = Meeting.objects.get(id=self.kwargs['meeting_id'])
        book = meeting.book
        context = super().get_context_data(**kwargs)
        context['book'] = book
        return context


class RecList(ListView):
    model = Book


class UserProfile(DetailView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']

@login_required
def clubs_index(request):
    clubs = Club.objects.all()


    return render(request, 'myclubs/index.html', { 'clubs': clubs, 'meetings': meetings })



@login_required
def club(request, club_id):
    club = Club.objects.get(id=club_id)
    return render(request, 'myclubs/club.html', { 'club': club})

@login_required
def meeting(request, club_id, meeting_id):
    club = Club.objects.get(id=club_id)
    meeting = Meeting.objects.get(id=meeting_id)
    book = meeting.book
    ratings = get_ratings(meeting_id, request.user.id)
    return render(request, 'myclubs/meeting.html', { 'club': club, 'meeting': meeting, 'book': book, 'ratings': ratings})

def get_ratings(meeting_id, user_id):
    meeting = Meeting.objects.get(id=meeting_id)
    book = meeting.book
    ratings = book.rating_set.all()
    if len(ratings) > 0:
        total = 0
        for r in ratings:
            total += r.rating
        average_rating = int(total/len(ratings))
        user_rating = ratings.filter(user_id=user_id)
        ratings = { 'average': int_to_star_string(average_rating), 'user' : int_to_star_string(user_rating[0].rating)}
    else:
        ratings = {'average': '', 'user':''}
    return ratings

def int_to_star_string(rating):
    stars = ''
    for r in range (rating):
        stars += '*'
    return stars


class ClubCreate(CreateView):
  model = Club
  fields = '__all__'
  success_url = '/clubs/'

