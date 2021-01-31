from django.shortcuts import render, redirect
import requests 
import os 
from .models import Book, Rec

# Create your views here.
def home(request):
    print("Working")

def select_book(request):
    books = None
    if request.GET: # isbn search
        if 'isbn' in request.GET:
            isbn = [request.GET['isbn']]
            books = search_isbn(isbn)
        elif 'search_title' in request.GET: # author/title search
            books = search_title_author(request.GET['search_title'], request.GET['search_author'])
    elif request.POST: # add selected title to database
        print(request.POST)
        print(request.POST['title'])
        new_book = Book(
            title=request.POST['title'],
            author=request.POST['author'],
            desc=request.POST['desc'],
            isbn=request.POST['isbn'],
            image=request.POST['image_link'],
            )
        # new_book.save()
        books = None
    return render(request, 'selectbook.html', { 'books' : books})

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
    isbn = [0]
    my_key = os.environ['GOOGLE_BOOKS_API_KEY']
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + search_title + '+inauthor:' + search_author +'&maxResults=' + str(MAX) + '&orderBy=relevance&printType=BOOKS&key=' + my_key).json()
    if r['totalItems'] < MAX:
        MAX = r['totalItems']
    for x in range(MAX):
        if 'industryIdentifiers' in r['items'][x]['volumeInfo']:
            num = r['items'][x]['volumeInfo']['industryIdentifiers'][0]['identifier']
            if num.isnumeric(): # filters out non-ISBN identifiers, which contain letter codes
                isbn.append(num)

    books = search_isbn(isbn)

    return books

# Some test ISBNs:
# 9781609618957
# 9780140441185
