from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from .models import BooksList, Author, BuyBook, BookImage
from .forms import BooksForm, BookImageForm, BookImageFormSet
# from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .permissions import delete_book_permission
from django.db.models import Q
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings

from django.views.generic import View, ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy

from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .mixins import BookAddMixin, BookEditMixin

from django.views.generic.edit import UpdateView

logger = logging.getLogger(__name__)

class BooksListView(ListView):
    model = BooksList
    template_name = 'events/books_list.html'
    context_object_name = 'books'
    paginate_by = 8
    # login_url = reverse_lazy('authentication:login')
    # permission_required = ('core.view_books',)

    def get_queryset(self):
        queryset = super().get_queryset()

        title = self.request.GET.get('title')
        author = self.request.GET.get('author')

        filters = Q()

        if title and author:
            filters &= Q(title__icontains=title) & (Q(author_id__first_name__icontains=author) | Q(author_id__last_name__icontains=author))
        elif title:
            filters |= Q(title__icontains=title)
        elif author:
            filters |= Q(author_id__first_name__icontains=author) | Q(author_id__last_name__icontains=author)

        if title or author:
            books = self.model.objects.filter(filters)
        else:
            books = self.model.objects.all()

        return books

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     context["test"] = "Satesto saxeli"
    #     # print("#################")
    #     # print(context)
    #     # print("#################")
    #
    #     return context


# def books_list(request):

    # logger.info('Started Index Page Logic')

#     title = request.GET.get('title')
#     author = request.GET.get('author')
#
#     # logger.warning(f'Filtering: Title - {title}, author - {author}')
#
#     filters = Q()
#
# if title and author:
#     filters &= Q(title__icontains=title) & (Q(author_id__first_name__icontains=author) | Q(author_id__last_name__icontains=author))
# elif title:
#     filters |= Q(title__icontains=title)
# elif author:
#     filters |= Q(author_id__first_name__icontains=author) | Q(author_id__last_name__icontains=author)
#
    # if title or author:
    #     books = filters
    # else:
    #     books = BooksList.objects.all()
#
#     # logger.info(f'Book Quantity: " {books.count()}')
#     paginator = Paginator(books, 4)
#     try:
#         page = request.GET.get('page')
#         books = paginator.page(page)
#     except PageNotAnInteger:
#         books = paginator.page(1)
#     except EmptyPage:
#         books = paginator.page(paginator.num_pages)
#
#     return render(request, 'events/books_list.html', {'books': books})


# @login_required(login_url='login')
# def add_book(request):
#     # if request.user.is_authenticated and request.user.has_perm('core.add_bookslist'):
#     # logger.info('Started Add Book Logic')
#
#     if request.method == 'POST':
#         image_formset = BookImageFormSet(request.POST, files=request.FILES)
#         book_form = BooksForm(request.POST)
#
#         if book_form.is_valid() and image_formset.is_valid():
#             book = book_form.save()
#
#             for image_form in image_formset:
#                 if image_form.cleaned_data.get('image'):
#                     image = image_form.save(commit=False)
#                     image.book = book
#                     image.save()
#
#         return redirect('books_list')
#     else:
#         book_form = BooksForm()
#         image_formset = BookImageFormSet()
#         return render(request, 'events/add_book.html', {'book_form': book_form, 'image_formset': image_formset})
#     # logger.info(f'Adding Book: Title - {title}')
#     # else:
#     #     return HttpResponse('You do not have permission to add books.')

class CreateBookView(BookAddMixin, CreateView):
    model = BooksList
    form_class = BooksForm
    template_name = 'events/add_book.html'
    success_url = reverse_lazy('core:books_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['image_formset'] = BookImageFormSet(queryset=BookImage.objects.none())

        return context

    def form_valid(self, form):
        book = form.save()

        image_formset = BookImageFormSet(self.request.POST, files = self.request.FILES)

        for image_form in image_formset:
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.book = book
                image.save()

        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

# def book_detail(request, pk):
#     # logger.info('Started Book Detail page Logic')
#
#     book = get_object_or_404(BooksList, pk=pk)
#     # logger.info(f'Book Detail Page: - {id}')
#
#     return render(request, 'events/book_detail.html', {'book': book})

class BookDetailView(DetailView):
    model = BooksList
    context_object_name = 'book'
    template_name = 'events/book_detail.html'


# @login_required(login_url='login')
# def buy_book(request, pk):
#     book = get_object_or_404(BooksList, pk=pk)
#
#     if book.sold_out():
#         return HttpResponse('The book is out stock.')
#
#     buy_book, created = BuyBook.objects.get_or_create(book=book, user=request.user)
#
#     if created:
#         buy_book.book_count = 1
#     else:
#         buy_book.book_count += 1
#
#     buy_book.save()
#
#     book.left_in_stock -= 1
#     book.save()
#
#     send_mail('Buy Book', f'{request.user.username} has successfully bought the book - {book.title}',
#               settings.DEFAULT_FROM_EMAIL, [request.user.email])
#     # send_mail('Buy Book', f'{request.user.username} has successfully bought the book - {book.title}.', settings.DEFAULT_FROM_EMAIL, [request.user.email])
#
#     return redirect('books_list')

class BuyBookView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(BooksList, pk=kwargs['pk'])

        if book.sold_out():
            return HttpResponse('The book is out of stock!')

        buy_book, created = BuyBook.objects.get_or_create(book=book, user=request.user)

        if created:
            buy_book.book_count = 1
        else:
            buy_book.book_count += 1

        buy_book.save()

        book.left_in_stock -= 1
        book.save()


        send_mail(
            'Buy Book',
            f'{request.user.username} has successfully bought the book - {book.title}',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email]
        )

        return redirect('core:books_list')
    # model = BooksList
    # success_url = reverse_lazy('core:books_list')
    #
    # def post(self, request, **kwargs):
    #     book_id = kwargs.get("book_id")
    #     book = get_object_or_404(BooksList, pk=book_id)



# @login_required(login_url='login')
# @delete_book_permission
# def delete_book(request, pk):
#     # logger.info('Started Delete Book Logic')
#
#     book = get_object_or_404(BooksList, pk=pk)
#     # book = BooksList.objects.get(pk=pk)
#     if request.method == 'POST':
#         book.delete()
#
#     # logger.info(f'Book - {id} has been deleted.')
#     return redirect('books_list')
#     # return HttpResponseRedirect(reverse('books_list'))

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = BooksList
    template_name = 'events/book_confirm_delete.html'
    success_url = reverse_lazy('core:books_list')


# def change_book(request, pk):
#     # logger.info('Edit Book Logic has started.')
#
#     book = get_object_or_404(BooksList, pk=pk)
#
#     if request.method == 'POST':
#         form = BooksForm(request.POST, instance=book)
#
#         if form.is_valid():
#             book = form.save()
#
#             return redirect('book_detail', pk=pk)
#
#     else:
#         form = BooksForm(instance=book)
#         return render(request, 'events/update_books.html', {'form': form})
#     # logger.info(f'Book - Title - {id} has been changed.')

class BookUpdateView(BookEditMixin, UpdateView):
    model = BooksList
    form_class = BooksForm
    template_name = 'events/update_books.html'

    def get_success_url(self):
        success_url = reverse_lazy('core:book_detail', kwargs={'pk': self.object.pk})
        return success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        BookImageFormSet = modelformset_factory(BookImage, form=BookImageForm, can_delete=True)

        book = self.get_object()

        queryset = book.images.all() if book.images.exists() else BookImage.objects.none()

        if self.request.POST:
            context['image_formset'] = BookImageFormSet(self.request.POST, files=self.request.FILES, queryset=queryset)
        else:
            context['image_formset'] = BookImageFormSet(queryset=self.queryset)

        return context


    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context.get('image_formset', None)

        if form.is_valid() and image_formset and image_formset.is_valid():
            self.object = form.save()
            images = image_formset.save(commit=False) or []

            for img in images:
                img.book = self.object
                img.save()

            return redirect(self.success_url)

        return self.form_invalid(form)