from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse_lazy
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse_lazy('home'))  # Redirect non-superusers to the home page
        return view_func(request, *args, **kwargs)
    return _wrapped_view