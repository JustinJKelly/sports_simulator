from django.contrib import admin
from .models import Player, Game, GameLog, Team, MVPPoll, Series, GamePreview

# Register your models here.
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(GameLog)
admin.site.register(Team)
admin.site.register(MVPPoll)
admin.site.register(Series)
admin.site.register(GamePreview)