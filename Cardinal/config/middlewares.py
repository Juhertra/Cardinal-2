from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

User = get_user_model()

class RoleBasedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        login_url = reverse('login')
        signup_url = reverse('signup')

        # Exclude login and signup URLs
        if request.path == login_url or request.path == signup_url:
            return None

        if not request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_URL)

        # Set user role
        try:
            request.user.role = request.user.groups.all()[0].name
        except IndexError:
            request.user.role = None

        if hasattr(view_func, 'allowed_roles'):
            if request.user.role not in view_func.allowed_roles:
                return HttpResponseForbidden('Forbidden')

        return None
