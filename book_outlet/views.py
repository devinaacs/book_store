from django.shortcuts import render, get_list_or_404
from .models import Book
from django.http import Http404
from django.db.models import Avg
# Create your views here.


def index(request):
    books = Book.objects.all().order_by("title")
    num_books = books.count()
    avg_rating = books.aggregate(Avg("rating"))
    
    return render(request, "book_outlet/index.html", {
        "books": books,
        "totatl_number_of_books": num_books,
        "average_rating": avg_rating['rating__avg']
    })

# def book_detail(request, id):
#     try:
#         book = Book.objects.get(pk=id)
#     except:
#         raise Http404
#     return render(request, "book_outlet/book_detail.html", {
#         "title": book.title,
#         "author": book.author,
#         "rating": book.rating,
#         "is_bestselling": book.is_bestselling
#     })

def book_detail(request, slug):
    book = get_list_or_404(Book, slug=slug)[0]
    return render(request, "book_outlet/book_detail.html", {
        "title": book.title,
        "author": book.author,
        "rating": book.rating,
        "is_bestselling": book.is_bestselling
    })