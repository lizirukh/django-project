from django.shortcuts import render, redirect
from .models import BooksList
from .forms import BooksForm


def books_list(request):

    books = BooksList.objects.all()
    return render(request, 'events/books_list.html', {'books': books})

def add_book(request):

    if request.method == 'POST':
        form = BooksForm(request.POST)

        if form.is_valid():
            book = form.save()

            return redirect('books_list')

    else:
        form = BooksForm()

        return render(request, 'events/add_book.html', {'form': form})
