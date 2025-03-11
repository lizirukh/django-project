from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from .models import BooksList, Author, BuyBook
from .forms import BooksForm, BookImageFormSet
# from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .permissions import delete_book_permission
from django.db.models import Q
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings


logger = logging.getLogger(__name__)

def books_list(request):

    # logger.info('Started Index Page Logic')

    title = request.GET.get('title')
    author = request.GET.get('author')

    # logger.warning(f'Filtering: Title - {title}, author - {author}')

    filters = Q()

    if title and author:
        filters &= Q(title__icontains=title) & (Q(author_id__first_name__icontains=author) | Q(author_id__last_name__icontains=author))
    elif title:
        filters |= Q(title__icontains=title)
    elif author:
        filters |= Q(author_id__first_name__icontains=author) | Q(author_id__last_name__icontains=author)

    if title or author:
        books = filters
    else:
        books = BooksList.objects.all()

    # logger.info(f'Book Quantity: " {books.count()}')
    paginator = Paginator(books, 4)
    try:
        page = request.GET.get('page')
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'events/books_list.html', {'books': books})

@login_required(login_url='login')
def add_book(request):

    # if request.user.is_authenticated and request.user.has_perm('core.add_bookslist'):
    # logger.info('Started Add Book Logic')

    if request.method == 'POST':
        image_formset = BookImageFormSet(request.POST, files=request.FILES)
        book_form = BooksForm(request.POST)

        if book_form.is_valid() and image_formset.is_valid():
            book = book_form.save()

            for image_form in image_formset:
                if image_form.cleaned_data.get('image'):
                    image = image_form.save(commit=False)
                    image.book = book
                    image.save()

        return redirect('books_list')
    else:
        book_form = BooksForm()
        image_formset = BookImageFormSet()
        return render(request, 'events/add_book.html', {'book_form': book_form, 'image_formset': image_formset})
    # logger.info(f'Adding Book: Title - {title}')
    # else:
    #     return HttpResponse('You do not have permission to add books.')

def book_detail(request, pk):
    # logger.info('Started Book Detail page Logic')

    book = get_object_or_404(BooksList, pk=pk)
    # logger.info(f'Book Detail Page: - {id}')

    return render(request, 'events/book_detail.html', {'book': book})

@login_required(login_url='login')
def buy_book(request, pk):
    book = get_object_or_404(BooksList, pk=pk)

    if book.sold_out():
        return HttpResponse('The book is out stock.')

    buy_book, created = BuyBook.objects.get_or_create(book = book, user = request.user)

    if created:
        buy_book.book_count = 1
    else:
        buy_book.book_count += 1

    buy_book.save()

    book.left_in_stock -= 1
    book.save()

    send_mail('Buy Book', f'{request.user.username} has successfully bought the book - {book.title}', settings.DEFAULT_FROM_EMAIL, [request.user.email])
    # send_mail('Buy Book', f'{request.user.username} has successfully bought the book - {book.title}.', settings.DEFAULT_FROM_EMAIL, [request.user.email])

    return redirect('books_list')


@login_required(login_url='login')
@delete_book_permission
def delete_book(request, pk):
    # logger.info('Started Delete Book Logic')

    book = get_object_or_404(BooksList, pk=pk)
    # book = BooksList.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()

    # logger.info(f'Book - {id} has been deleted.')
    return redirect('books_list')
    # return HttpResponseRedirect(reverse('books_list'))


def change_book(request, pk):
    # logger.info('Edit Book Logic has started.')

    book = get_object_or_404(BooksList, pk=pk)

    if request.method == 'POST':
        form = BooksForm(request.POST, instance=book)

        if form.is_valid():
            book = form.save()

            return redirect('book_detail', pk=pk)

    else:
        form = BooksForm(instance=book)
        return render(request, 'events/update_books.html', {'form': form})
    # logger.info(f'Book - Title - {id} has been changed.')
