from django.http import HttpResponseForbidden
from django.conf import settings
from functools import wraps

def allowed_roles(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden()

            user_groups = user.groups.values_list('name', flat=True)
            if not set(allowed_roles).intersection(user_groups):
                return HttpResponseForbidden()

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
