from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.models import BooksList, BookImage
from .serializers import BooksListSerializer

from rest_framework.generics import get_object_or_404

@api_view(['GET'])
def test(request):
    return Response({"message": 'API created successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def books_list(request):
    books = BooksList.objects.all()

    serializer = BooksListSerializer(books, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_book(request):
    serializer = BooksListSerializer(data=request.data)

    if serializer.is_valid():
        book = serializer.save()

        images = request.FILES.getlist('images')
        for image in images:
            BookImage.objects.create(book=book, image=image)

        return Response({'message': "book was added successfully"})

    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['DELETE'])
def delete_book(request, pk):
    book = get_object_or_404(BooksList, pk=pk)
    book.delete()

    return Response({'message': 'Book was deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update_book(request, pk):
    book = get_object_or_404(BooksList, pk=pk)
    book_serializer = BooksListSerializer(book, data=request.data)

    if book_serializer.is_valid():
        book_serializer.save()

        return Response({'message': f"Book id: {pk} - was updated successfully. f'Book': {book_serializer.data}"}, status=status.HTTP_200_OK )

    return Response(book_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)