from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden

class BookAddMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.has_perm('core.add_bookslist'):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

class BookEditMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.has_perm('core.change_bookslist'):
            return HttpResponseForbidden("You do not have permission to edit details of the book.")
        return super().dispatch(request, *args, **kwargs)