from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from .models import BooksList
from .forms import BooksForm
from django.urls import reverse
from .permissions import delete_book_permission

from .permissions import delete_book_permission


def books_list(request):

    query = request.GET.get('search_item')

    if query:
        books = BooksList.objects.filter(title__icontains=query)
    else:
        books = BooksList.objects.all()

    return render(request, 'events/books_list.html', {'books': books})

def add_book(request):

    # if request.user.is_authenticated and request.user.has_perm('core.add_bookslist'):

    if request.method == 'POST':
        form = BooksForm(request.POST)

        if form.is_valid():
            book = form.save()

            return redirect('books_list')

    else:
        form = BooksForm()
        return render(request, 'events/add_book.html', {'form': form})

    # else:
    #     return HttpResponse('You do not have permission to add books.')

def book_detail(request, pk):
    book = get_object_or_404(BooksList, pk=pk)

    return render(request, 'events/book_detail.html', {'book': book})

@delete_book_permission
def delete_book(request, pk):
    book = BooksList.objects.get(pk=pk)
    book.delete()

    return HttpResponseRedirect(reverse('books_list'))
