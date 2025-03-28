from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('add/', views.add_book, name='add_book' ),
    path('book/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('book/update/<int:pk>/', views.update_book, name='update_book'),
]