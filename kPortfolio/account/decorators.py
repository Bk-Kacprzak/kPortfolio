from django.core.exceptions import PermissionDenied
from django.shortcuts import HttpResponseRedirect


def user_not_logged_in(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")  # redirect to home page

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
