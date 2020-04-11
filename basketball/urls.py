from django.urls import path, include
from . import views

urlpatterns = [
    #basketball/-- return basketball home page so get into other views.py and call home
    path('', views.home, name='basketball_home'), 
]