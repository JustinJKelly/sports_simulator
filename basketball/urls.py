from django.urls import path, include
from . import views
from basketball import views


urlpatterns = [
    #basketball/-- return basketball home page so get into other views.py and call home
    path('games/<int:game_date>', views.get_games_date, name='get_games_date'), 
    path('games_mobile/<int:game_date>', views.get_games_date_mobile, name='get_games_date_mobile'), 
    path('games', views.home, name='games_home'), 
    path('games_mobile', views.home_mobile, name='games_home_mobile'), 
    path('player/<int:id>', views.player_page, name="player_page"),
    path('player_mobile/<int:id>', views.player_page_mobile, name="player_page_mobile"),
    path('game/<int:id>', views.game_page, name="game_page"),
    path('game_mobile/<int:id>', views.game_page_mobile, name="game_page_mobile"),
    path('teams', views.team_home_page, name="teams_home"),
    path('teams_mobile', views.team_home_page_mobile, name="teams_home_mobile"),
    path('team/<int:id>', views.team_page, name="teams_page"),
    path('team_mobile/<int:id>', views.team_page_mobile, name="teams_page_mobile"),
    path('standings', views.standings_page, name="standings_page"),
    path('standings_mobile', views.standings_page_mobile, name="standings_page_mobile"),
    path('playoffs', views.playoffs_page, name="playoffs_page"),
    path('playoffs_mobile', views.playoffs_page_mobile, name="playoffs_page_mobile"),
    path('playoffs/series/<int:id>', views.series_page, name="series_page"),
    path('playoffs/series_mobile/<int:id>', views.series_page_mobile, name="series_page_mobile"),
    path('mvp_vote', views.mvp_vote, name="mvp_vote"),
    path('mvp_vote_mobile', views.mvp_vote_mobile, name="mvp_vote_mobile"),
    path('mvp_results', views.mvp_results, name="mvp_results"),
    path('mvp_results_mobile', views.mvp_results_mobile, name="mvp_results_mobile"),
    path('series_vote', views.series_vote, name="series_vote"),
    path('series_vote_mobile', views.series_vote_mobile, name="series_vote_mobile"),
    path('series_vote_results', views.series_vote_results, name="series_vote_results"),
    path('series_vote_results_mobile', views.series_vote_results_mobile, name="series_vote_results_mobile"),
]