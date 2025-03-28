from rest_framework import serializers
from core.models import BooksList

class BooksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksList
        fields = '__all__'
        # fields = ('title', )