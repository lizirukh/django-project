from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path('', views.books_list, name='books_list'),
    path('', views.BooksListView.as_view(), name='books_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('book/change/<int:pk>/', views.change_book, name='change_book'),
    path('book/buy/<int:pk>/', views.buy_book, name='buy_book'),
]