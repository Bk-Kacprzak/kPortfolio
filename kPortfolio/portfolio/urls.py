from django.urls import path
from . import views


urlpatterns = [
    path("", views.PortfolioCreateView.as_view(), name='portfolio'),
    path("overview", views.OverviewPanelView.as_view(), name='portfolio_overview'),
]

