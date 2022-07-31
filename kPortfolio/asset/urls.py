from django.contrib import admin
from django.urls import path, include
from kPortfolio.main import views as main_view
from .views import *

urlpatterns = [
    path(r'load-new-assets/', load_asset_data),
    path(r'update-assets/', update_asset_data)
]