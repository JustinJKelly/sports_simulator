from django import forms
from .models import MVPVote, GamePreview
from . import views

global gid

class MVPVoteForm(forms.Form):
    mvp_poll = MVPVote.objects.all().order_by('-votes','-points_pg')
    CHOICES = []
    for player in mvp_poll:
        CHOICES.append( (player.player_id,(player.player_name + '    ' + player.team_abv)) )
    VOTE_FOR_MVP = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='')
    
    
    def __init__(self, *args, **kwargs):
        super(MVPVoteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['style'] = 'width:45%;'
            visible.field.widget.attrs['onfocus'] = "this.size=15;"
            visible.field.widget.attrs['onblur'] = "this.size=1;"
            visible.field.widget.attrs['onchange'] = "this.size=1; this.blur();"

'''
    game_date = models.DateField(default=date.today)
    home_team_id = models.IntegerField(null=False)
    away_team_id = models.IntegerField(null=False)
    higher_seeding_id = models.IntegerField(null=False)
    lower_seeding_id = models.IntegerField(null=False)
    higher_seeding_name = models.CharField(max_length=35,null=False)
    lower_seeding_name = models.CharField(max_length=35,null=False)
    home_team_name = models.CharField(max_length=35,null=False)
    away_team_name = models.CharField(max_length=35,null=False)
    game_preview_id = models.IntegerField(primary_key=True)
    votes_home_team = models.IntegerField(default=0)
    votes_home_away = models.IntegerField(default=0)
'''

class GamePreviewForm(forms.Form):
    
    games = GamePreview.objects.all()
    for game in games:
        CHOICES = [
            (('%s %s' % (game.home_team_id,game.game_preview_id)), game.home_team_name), 
            (('%s %s' % (game.away_team_id,game.game_preview_id)), game.away_team_name,)
        ]
    form = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='')
