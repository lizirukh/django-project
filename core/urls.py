from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('book/add/', views.add_book, name='add_book'),
]