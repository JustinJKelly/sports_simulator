from django.urls import path, include
from . import views
from basketball import views


urlpatterns = [
    #basketball/-- return basketball home page so get into other views.py and call home
    path('games/<int:game_date>', views.get_games_date, name='get_games_date'), 
    path('games', views.home, name='games_home'), 
    path('player/<int:id>', views.player_page, name="player_page"),
    path('game/<int:id>', views.game_page, name="game_page"),
    path('teams', views.team_home_page, name="teams_home"),
    path('team/<int:id>', views.team_page, name="teams_page"),
    path('team/standings', views.standings_page, name="standings_page"),
    path('playoffs', views.playoffs_page, name="playoffs_page"),
    path('playoffs/series/<int:id>', views.series_page, name="series_page"),
    path('mvp_vote', views.mvp_vote, name="mvp_vote"),
    path('mvp_results', views.mvp_results, name="mvp_results"),
    path('series_vote', views.series_vote, name="series_vote"),
    path('series_vote_results', views.series_vote_results, name="series_vote_results"),
]