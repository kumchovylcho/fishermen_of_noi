from django.shortcuts import redirect
from django.urls import reverse


class AdminRestrictMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_authenticated or not request.user.is_superuser:
                return redirect('home')
        return self.get_response(request)