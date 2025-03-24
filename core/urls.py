from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path('', views.books_list, name='books_list'),
    path('', views.BooksListView.as_view(), name='books_list'),
    # path('add_book/', views.add_book, name='add_book'),
    path('add_book/', views.CreateBookView.as_view(), name='add_book'),
    # path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    # path('book/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('book/delete/<int:pk>/', views.BookDeleteView.as_view(), name='delete_book'),
    # path('book/change/<int:pk>/', views.change_book, name='change_book'),
    path('book/change/<int:pk>/', views.BookUpdateView.as_view(), name='change_book'),
    # path('book/buy/<int:pk>/', views.buy_book, name='buy_book'),
    path('book/buy/<int:pk>/', views.BuyBookView.as_view(), name='buy_book'),
]