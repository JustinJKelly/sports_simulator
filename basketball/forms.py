from django import forms
from .models import MVPPoll
from . import views

class MVPPollForm(forms.Form):
    mvp_poll = MVPPoll.objects.all().first()
    data = mvp_poll.data
    CHOICES = []
    for key,values in data:
        CHOICES.append( (key,[values['name'],values['team_abv'],values['team_image'],values['team_id'],values['player_id']]) )
    #print(CHOICES)
    VOTE_FOR_MVP = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    