from django.urls import path
from . import views
urlpatterns = [
    path("register/", views.register_request, name='register'),
    path("login/", views.login_request, name='login'),
    path("logout/", views.logout_request, name='logout'),
    path("forgot/", views.forgot_request, name='forgot'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.activate, name='activate'),
    path("email-confirmation/", views.email_confirmation, name='email_confirmation'),
]