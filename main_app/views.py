from django.shortcuts import render, redirect
import requests 

ISBN_ROOT = 'https://openlibrary.org/api/books'

# Create your views here.
def home(request):
    print("Working")


def select_book(request):
    if 'isbn' in request.GET:
        book = search_isbn(request.GET['isbn'])
    # print('Body: ', request.GET['isbn'])
    else:
        book = None
    return render(request, 'selectbook.html', { 'book' : book})



def search_isbn(isbn): # takes an ISBN number and returns an object containing book, author, isbn, and image_link 
    r = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:' + str(isbn) +'&jscmd=data&format=json').json()
    # r = requests.get(ISBN_ROOT, params={'ISBN': isbn, 'format':'json', 'jscmd':'data'}).json()
    isbn_key = 'ISBN:' + str(isbn)
    if isbn_key in r:
        title = r[isbn_key]['title']
        author = r[isbn_key]['authors'][0]['name']

        if 'cover' in r[isbn_key]:
            image_link = r[isbn_key]['cover']['medium']
            print(r[isbn_key]['cover']['medium'])
        else:
            image_link = None

        book = {
            'title': title,
            'author': author,
            'image_link': image_link,
            'isbn' : isbn,
        }

    else:
        book = { 'error' : 'ISBN not found. Please check your search and try again'}

    return book



# 9781609618957
# 9780140441185