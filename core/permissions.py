from django.http import HttpResponseForbidden

def delete_book_permission(function):
    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.delete_bookslist'):
            return function(request, *args, **kwargs)

        else:
            return HttpResponseForbidden("You do not have permission to delete this book.")

    return wrapper

def change_book_permission(function):
    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.change_bookslist'):
            return function(request, *args, **kwargs)

        else:
            return HttpResponseForbidden("You do not have permission to update this book.")

    return wrapper