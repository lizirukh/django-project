from django import forms
from .models import BooksList

class BooksForm(forms.ModelForm):
    class Meta:
        model = BooksList
        fields = '__all__'