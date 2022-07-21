from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('forgot/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>', views.reset_password, name='reset_password'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]