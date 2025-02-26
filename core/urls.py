from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
]