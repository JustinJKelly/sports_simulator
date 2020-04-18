from django.urls import path, include
from . import views
from basketball import views


urlpatterns = [
    #basketball/-- return basketball home page so get into other views.py and call home
    path('', views.home, name='basketball_home'), 
    path('player/<int:id>', views.player_page, name="player_page"),
    path('game/<int:id>', views.game_page, name="game_page")
]