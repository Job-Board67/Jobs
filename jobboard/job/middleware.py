from django.shortcuts import redirect
from django.conf import settings

EXEMPT_URLS = [
    settings.LOGIN_URL,
    "/register/",          
    "/accounts/logout/",
    "/admin/",
    "/static/", 
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if not request.user.is_authenticated:
            if not any(path.startswith(url) for url in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)
