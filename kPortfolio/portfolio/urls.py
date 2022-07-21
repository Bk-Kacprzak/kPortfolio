from django.urls import path
from . import views


urlpatterns = [
    path("", views.portfolio, name='portfolio'),
    path("overview", views.portfolio_overview, name='portfolio_overview'),
]

