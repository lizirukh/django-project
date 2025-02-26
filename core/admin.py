from django.contrib import admin
from .models import BooksList, Category

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publishing_date', 'create_date')
    search_fields = ('title',)
    list_filter = ('genre',)

admin.site.register(BooksList, BookAdmin)
admin.site.register(Category)
