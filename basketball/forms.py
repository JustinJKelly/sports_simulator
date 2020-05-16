from django import forms
from .models import MVPVote, Serie
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
    
    