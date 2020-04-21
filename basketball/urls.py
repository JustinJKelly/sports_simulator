from django.urls import path, include
from . import views
from basketball import views


urlpatterns = [
    #basketball/-- return basketball home page so get into other views.py and call home
    path('game', views.home, name='games_home'), 
    path('player/<int:id>', views.player_page, name="player_page"),
    path('game/<int:id>', views.game_page, name="game_page"),
    path('teams', views.team_home_page, name="teams_home"),
    path('team/<int:id>', views.team_page, name="teams_page"),
    path('team/standings', views.standings_page, name="standings_page"),
    path('playoffs', views.playoffs_page, name="playoffs_page")
]