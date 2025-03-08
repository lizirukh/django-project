from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

class Author(models.Model):

    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField(null=True)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class BooksList(models.Model):

    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books_list', null=False)
    genre = models.ManyToManyField(Category, related_name='books_list', null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    publishing_date = models.DateField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books_list'

    def __str__(self):
        return self.title, self.author

class BookImage(models.Model):
    book = models.ForeignKey(BooksList, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='book-images/', null=True, blank=True)