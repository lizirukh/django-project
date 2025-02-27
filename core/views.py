from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from .models import BooksList, Author
from .forms import BooksForm
# from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .permissions import delete_book_permission
from django.db.models import Q



def books_list(request):

    query1 = request.GET.get('search_item2')
    query2 = request.GET.get('search_item2')

    if query1 and query2:
        books1 = BooksList.objects.filter(title__icontains=query1)
        books2 = BooksList.objects.filter(Q(author__first_name__icontains=query2) | Q(author__last_name__icontains=query2))
        books = books1 & books2
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

@login_required(login_url='login')
@delete_book_permission
def delete_book(request, pk):
    book = get_object_or_404(BooksList, pk=pk)
    # book = BooksList.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()

    return redirect('books_list')
    # return HttpResponseRedirect(reverse('books_list'))


def change_book(request, pk):
    book = get_object_or_404(BooksList, pk=pk)

    if request.method == 'POST':
        form = BooksForm(request.POST, instance=book)

        if form.is_valid():
            book = form.save()

            return redirect('book_detail', pk=pk)

    else:
        form = BooksForm(instance=book)
        return render(request, 'events/update_books.html', {'form': form})