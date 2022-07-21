"""kPortfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.main, name='main')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='main')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from kPortfolio.main import views as main_view

urlpatterns = [
    path(r'admin/', admin.site.urls),
    # path('api/', include('api.urls')),
    path(r'account/', include('kPortfolio.account.urls')),
    path(r'', main_view.index, name='index'),
    path(r'portfolio', include('kPortfolio.portfolio.urls')),
]
