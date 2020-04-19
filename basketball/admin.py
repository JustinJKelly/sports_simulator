from django.contrib import admin
from .models import Player, Game, GameLog, Team

# Register your models here.
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(GameLog)
admin.site.register(Team)