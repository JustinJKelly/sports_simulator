from basketball.models import Game,GamePreview, Team, Serie
from datetime import date

def make_game_previews():
    
    day = 12
    series = Serie.objects.all()
    
    for serie in series:
        
        for count in range (1,8):
            game_date_start = date(2020,5,day)
        
            if count == 1 or count == 2 or count == 5 or count == 7:
                home_team = serie.higher_seed_id
                home_name = serie.higher_seed_name
                away_team = serie.lower_seed_id
                away_name = serie.lower_seed_name
            
            else:
                away_team = serie.higher_seed_id
                away_name = serie.higher_seed_name
                home_team = serie.lower_seed_id
                home_name = serie.lower_seed_name
            
            if len(GamePreview.objects.all())==0:
                game_preview_id = 0
            else:
                game_preview_id = (GamePreview.objects.all().order_by('-game_preview_id')[0].game_preview_id+1)
            print(game_preview_id)
            
            if count < 5:
                is_nec = True
            else:
                is_nec = False
            
            game_preview = GamePreview(game_date=game_date_start,home_team_id=home_team,away_team_id=away_team,
                                   higher_seeding_id=serie.higher_seed_id,lower_seeding_id=serie.lower_seed_id,
                                   higher_seeding_name=serie.higher_seed_name,lower_seeding_name=serie.lower_seed_name,
                                   home_team_name=home_name,away_team_name=away_name,
                                   game_preview_id=game_preview_id,series=serie,is_necessary=is_nec)
        
            game_preview.save()
            day += 1
        
        day = 12
        
    
    