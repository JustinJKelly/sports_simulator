"""sports_simulator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.away, name='away')
Class-based views
    1. Add an import:  from other_app.views import away
    2. Add a URL to urlpatterns:  path('', away.as_view(), name='away')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
    path('whatissportssim', views.articles_sports_sim, name="whatissportssim"),
    path('voting', views.articles_voting, name="voting"),
    path('playoffs', views.articles_playoffs, name="playoffs"),
    path('basketball/',include('basketball.urls')),
    re_path(r'^.*/$',views.path_does_not_exist, name="path_dne")
]