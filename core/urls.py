from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('add_book/', views.add_book, name='add_book'),
]