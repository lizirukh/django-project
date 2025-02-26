from django.http import HttpResponseForbidden

def delete_book_permission(function):
    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.delete_bookslist'):
            return function(request, *args, **kwargs)

        else:
            return HttpResponseForbidden("You do not have permission to delete this book.")

    return wrapper