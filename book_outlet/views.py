from django.shortcuts import render
from .models import Book
from django.http import Http404
# Create your views here.


def index(request):
    books = Book.objects.all()
    return render(request, "book_outlet/index.html", {
        "books": books
    })

def book_detail(request, id):
    try:
        book = Book.objects.get(pk=id)
    except:
        raise Http404
    return render(request, "book_outlet/book_detail.html", {
        "title": book.title,
        "author": book.author,
        "rating": book.rating,
        "is_bestselling": book.is_bestselling
    })