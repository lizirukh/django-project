from django import forms
from .models import BooksList, BookImage


class BooksForm(forms.ModelForm):
    class Meta:
        model = BooksList
        fields = '__all__'

class BookImageForm(forms.ModelForm):
    class Meta:
        model = BookImage
        fields = ('image',)

BookImageFormSet =forms.modelformset_factory(BookImage, form=BookImageForm, extra=2, can_delete=True)