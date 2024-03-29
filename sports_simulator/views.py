from django.shortcuts import redirect, render
from basketball.models import Game,Team, Counter,GamePreview
from django.http import HttpResponse
import datetime


def path_does_not_exist(request):
    return render(request,"error_request.html")

def home(request):
    print("here")
    '''counter = Counter.objects.all()[0]
    counter.countVisitors += 1
    counter.save()
    context= dict()
    today = datetime.date.today()
    print(datetime.datetime.now().hour)
    if datetime.datetime.now().hour < 14:
        games = GamePreview.objects.filter(game_date=today)
        context['games']=[]
        count = 1
        for game in games:
            context['games'].append([
                game.game_preview_id,
                Team.objects.get(team_id=game.away_team_id).team_abv,
                Team.objects.get(team_id=game.home_team_id).team_abv,
                find_team_image(game.away_team_id),
                find_team_image(game.home_team_id),
                ("%s/%s/%s" % (today.month,today.day,today.year))
            ])
            count+=1
    else:
        played_games = Game.objects.filter(date=today)
        context['played_games']=[]
        count = 1
        for game in played_games:
            context['played_games'].append([
                game.game_id,
                Team.objects.get(team_id=game.away_team).team_abv,
                Team.objects.get(team_id=game.home_team).team_abv,
                find_team_image(game.away_team),
                find_team_image(game.home_team),
                ("%s/%s/%s" % (today.month,today.day,today.year))
            ])
            count+=1'''
    return redirect("/basketball/teams")
    #return render(request, 'base.html', {})

def articles_sports_sim(request):
    return render(request, 'article_whatissportssim.html')

def articles_playoffs(request):
    return render(request, 'article_playoffs.html')

def articles_voting(request):
    return render(request, 'article_voting.html')

def find_team_image(team_id):
    list_teams = {
        1610612737:"img/atlanta-hawks.png",
        1610612738:"img/boston-celtics.png",
        1610612751:"img/brooklyn-nets.png",
        1610612766:"img/charlotte-hornets.png",
        1610612741:"img/chicago-bulls.png",
        1610612739:"img/cleveland-cavaliers.png",
        1610612742:"img/dallas-mavericks.png",
        1610612743:"img/denver-nuggets.png",
        1610612765:"img/detroit-pistons.png",
        1610612744:"img/golden-state-warriors.png",
        1610612745:"img/houston-rockets.png",
        1610612754:"img/indiana-pacers.png",
        1610612746:"img/los-angeles-clippers.png",
        1610612747:"img/los-angeles-lakers.png",
        1610612763:"img/memphis-grizzlies.png",
        1610612748:"img/miami-heat.png",
        1610612749:"img/milwaukee-bucks.png",
        1610612750:"img/minnesota-timberwolves.png",
        1610612740:"img/new-orleans-pelicans.png",
        1610612752:"img/new-york-knicks.png",
        1610612760:"img/oklahoma-city-thunder.png",
        1610612753:"img/orlando-magic.png",
        1610612755:"img/philadelphia-76ers.png",
        1610612756:"img/phoenix-suns.png",
        1610612757:"img/portland-trail-blazers.png",
        1610612758:"img/sacramento-kings.png",
        1610612759:"img/san-antonio-spurs.png",
        1610612761:"img/toronto-raptors.png",
        1610612762:"img/utah-jazz.png",
        1610612764:"img/washington-wizards.png",
        0:"img/nba_logo.png"
    }
    return list_teams[team_id]