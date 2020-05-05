from django import forms
from .models import MVPVote
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
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['style'] = 'width:45%;'
            visible.field.widget.attrs['onfocus'] = "this.size=15;"
            visible.field.widget.attrs['onblur'] = "this.size=1;"
            visible.field.widget.attrs['onchange'] = "this.size=1; this.blur();"