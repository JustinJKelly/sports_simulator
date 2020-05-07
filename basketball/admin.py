from django.contrib import admin
from .models import Player, Game, Serie, MVPVote,Team, GamePreview

# Register your models here.
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Team)
admin.site.register(Serie)
admin.site.register(GamePreview)
admin.site.register(MVPVote)