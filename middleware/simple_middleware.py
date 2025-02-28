from django.utils.timezone import now

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f'[ Request: {request.path} {now()}]')

        response = self.get_response(request)

        print(f'[ Response: {request.path} {now()}]')

        return response
