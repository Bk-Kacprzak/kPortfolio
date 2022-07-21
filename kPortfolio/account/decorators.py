from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponseRedirect


def user_not_logged_in(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")  # redirect to home page

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

# def user_activated(function):
#     def wrap(request, *args, **kwargs):
#         if request.user.email_activated:
#             return function(request, *args, **kwargs)
#
#         return render(request, 'account/auth/verify-email.html')
#
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap
