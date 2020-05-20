from django import forms
from .models import MVPVote, Serie, Team
from . import views


class MVPVoteForm(forms.Form):
    mvp_poll = MVPVote.objects.all().order_by('-votes','-points_pg')
    CHOICES = []
    for player in mvp_poll:
        CHOICES.append( (player.player_id,(player.player_name + '    ' + player.team_abv)) )
    VOTE_FOR_MVP = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='')
    
    
    def __init__(self, *args, **kwargs):
        super(MVPVoteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            #visible.field.widget.attrs['class'] = 'form-control'
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



class SeriesForm(forms.Form):
    series = Serie.objects.all()
    CHOICES = []
    count = 0
    for serie in series:
        CHOICES = []
        if serie.current:
            CHOICES.append(
                (('%s %s' % (serie.higher_seed_id,serie.series_id), serie.higher_seed_name))
            )
            CHOICES.append(
                (('%s %s' % (serie.lower_seed_id,serie.series_id), serie.lower_seed_name))
            )
            if count == 0:
                form = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='%s vs. %s' % (serie.higher_seed_abv, serie.lower_seed_abv))
            elif count == 1:
                form1 = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='%s vs. %s' % (serie.higher_seed_abv, serie.lower_seed_abv))
            elif count == 2:
                form2 = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='%s vs. %s' % (serie.higher_seed_abv, serie.lower_seed_abv))
            elif count == 3:
                form3 = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='%s vs. %s' % (serie.higher_seed_abv, serie.lower_seed_abv))
            elif count == 4:
                form4 = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='%s vs.%s' % (serie.higher_seed_abv, serie.lower_seed_abv))
            elif count == 5:
                form5 = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='%s vs. %s' % (serie.higher_seed_abv, serie.lower_seed_abv))
            elif count == 6:
                form6 = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='%s vs. %s' % (serie.higher_seed_abv, serie.lower_seed_abv))
            elif count == 7:
                form7 = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='%s vs. %s' % (serie.higher_seed_abv, serie.lower_seed_abv))
            
            count += 1
    
    
class PlayoffForm(forms.Form):
    eastern_teams = Team.objects.filter(conference="East").order_by("-team_wins")
    western_teams = Team.objects.filter(conference="West").order_by("-team_wins")
    
    #West
    CHOICES_WEST = []
    
    for team in western_teams:
        CHOICES_WEST.append(
                    ((team.team_id, team.team_name))
                )
    first_seed_west = forms.ChoiceField(choices=CHOICES_WEST, widget=forms.Select,initial=western_teams[0].team_id, label='Pick 1st Seed West')
    second_seed_west = forms.ChoiceField(choices=CHOICES_WEST, widget=forms.Select,initial=western_teams[1].team_id, label='Pick 2nd Seed West')
    third_seed_west = forms.ChoiceField(choices=CHOICES_WEST, widget=forms.Select,initial=western_teams[2].team_id, label='Pick 3rd Seed West')
    fourth_seed_west = forms.ChoiceField(choices=CHOICES_WEST, widget=forms.Select,initial=western_teams[3].team_id, label='Pick 4th Seed West')
    fifth_seed_west = forms.ChoiceField(choices=CHOICES_WEST, widget=forms.Select,initial=western_teams[4].team_id, label='Pick 5th Seed West')
    sixth_seed_west = forms.ChoiceField(choices=CHOICES_WEST, widget=forms.Select,initial=western_teams[5].team_id, label='Pick 6th Seed West')
    seventh_seed_west = forms.ChoiceField(choices=CHOICES_WEST, widget=forms.Select,initial=western_teams[6].team_id, label='Pick 7th Seed West')
    eighth_seed_west = forms.ChoiceField(choices=CHOICES_WEST, widget=forms.Select,initial=western_teams[7].team_id, label='Pick 8th Seed West')

    
    #East
    CHOICES_EAST = []
    
    for team in eastern_teams:
        CHOICES_EAST.append(
                    ((team.team_id, team.team_name))
                )
    first_seed_east = forms.ChoiceField(choices=CHOICES_EAST,initial=eastern_teams[0].team_id, widget=forms.Select, label='Pick 1st Seed East')
    second_seed_east = forms.ChoiceField(choices=CHOICES_EAST,initial=eastern_teams[1].team_id, widget=forms.Select, label='Pick 2nd Seed East')
    third_seed_east = forms.ChoiceField(choices=CHOICES_EAST,initial=eastern_teams[2].team_id, widget=forms.Select, label='Pick 3rd Seed East')
    fourth_seed_east = forms.ChoiceField(choices=CHOICES_EAST,initial=eastern_teams[3].team_id, widget=forms.Select, label='Pick 4th Seed East')
    fifth_seed_east = forms.ChoiceField(choices=CHOICES_EAST,initial=eastern_teams[4].team_id, widget=forms.Select, label='Pick 5th Seed East')
    sixth_seed_east = forms.ChoiceField(choices=CHOICES_EAST,initial=eastern_teams[5].team_id, widget=forms.Select, label='Pick 6th Seed East')
    seventh_seed_east = forms.ChoiceField(choices=CHOICES_EAST,initial=eastern_teams[6].team_id, widget=forms.Select, label='Pick 7th Seed East')
    eighth_seed_east = forms.ChoiceField(choices=CHOICES_EAST,initial=eastern_teams[7].team_id, widget=forms.Select, label='Pick 8th Seed East')
    