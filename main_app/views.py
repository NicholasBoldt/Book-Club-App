from django.shortcuts import render, redirect
import requests 
import os 
from .models import Book, Rec

ISBN_ROOT = 'https://openlibrary.org/api/books'

# Create your views here.
def home(request):
    print("Working")


def select_book(request):
    books = None
    if request.GET:
        if 'isbn' in request.GET:
            isbn = [request.GET['isbn']]
            books = search_isbn(isbn)
        # print('Body: ', request.GET['isbn'])
        elif 'search_title' in request.GET:
            books = search_title_author(request.GET['search_title'], request.GET['search_author'])

    elif request.POST:
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

def search_isbn(isbn_list): # takes a list of ISBN numbers and returns a list of objects containing book, author, isbn, desc and image_link 
    books = []
    my_key = os.environ['GOOGLE_BOOKS_API_KEY']
    for i, isbn in enumerate(isbn_list):
        print('ISBN is: ', isbn)
        # r = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:' + str(isbn) +'&jscmd=data&format=json').json()
        # isbn_key = 'ISBN:' + str(isbn)
        # if isbn_key in r:
        #     title = r[isbn_key]['title']
        #     author = r[isbn_key]['authors'][0]['name']
        #     print(title)
        #     if 'cover' in r[isbn_key]:
        #         image_link = r[isbn_key]['cover']['medium']
        #     else:
        #         image_link = None
        #     books.append({
        #         'title': title,
        #         'author': author,
        #         'image_link': image_link,
        #         'isbn' : isbn,
        #     })
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(isbn) + '&printType=BOOKS&key=' + my_key).json()
        if r['totalItems'] == 0:
            books.append({ 'error' : 'ISBN not found. Please check your search and try again'})
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

        # else:
        #     books.append({ 'error' : 'ISBN not found. Please check your search and try again'})



    return books

def search_title_author(search_title, search_author):
    MAX = 5 #maximum titles to return
    isbn = []
    my_key = os.environ['GOOGLE_BOOKS_API_KEY']
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + search_title + '+inauthor:' + search_author +'&maxResults=' + str(MAX) + '&orderBy=relevance&printType=BOOKS&key=' + my_key).json()
    # r = requests.get('https://www.googleapis.com/books/v1/volumes?q=Wizard+inauthor:Frank&maxResults=5&orderBy=relevance&printType=BOOKS&key=AIzaSyBCwPi28d-g2G8eaYfWVPYsbibwOaerf88').json()
    # print('Searching...')

    for x in range(5):
        if 'industryIdentifiers' in r['items'][x]['volumeInfo']:
            num = r['items'][x]['volumeInfo']['industryIdentifiers'][0]['identifier']
            if num.isnumeric(): # filters out non-ISBN identifiers, which contain letter codes
                isbn.append(num)



    books = search_isbn(isbn)

    return books





# 9781609618957
# 9780140441185
