from django.shortcuts import redirect
from django.urls import reverse

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            if request.path not in [reverse('login'), reverse('activate_account'), reverse('register')]:
                return redirect('activation_required')
        return self.get_response(request)
