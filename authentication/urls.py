from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.register_user, name='registration')
]