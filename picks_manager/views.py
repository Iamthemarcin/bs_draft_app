from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import requests
from io import BytesIO
from django.conf import settings
from picks_manager.models import Map, Mode
from homepage.views import search_response
# Create your views here.

def brawler_picks(request, brawler):
    print(brawler)
    return JsonResponse({'context': brawler})

def update_brawler_pics():
    all_brawlers_request = requests.get('https://api.brawlapi.com/v1/brawlers')
    all_brawlers_json = all_brawlers_request.json()
    contents = []
    for brawler in all_brawlers_json['list']:
        img_url = brawler['imageUrl']
        session_obj = requests.Session()
        response = session_obj.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
        image = Image.open(BytesIO(response.content))
        width, height = image.size
        crop_length = 25
        left,top,right,bottom = crop_length, crop_length, width-crop_length,height-crop_length
        image = image.crop((left,top,right,bottom))
        image.save('{}/images/brawlers/{}.png'.format(settings.STATICFILES_DIRS[0],brawler['name']), 'PNG')
    return HttpResponse(contents, content_type='image/png')


def update_map_list(): #allright, so there isnt any way to get the current power league map rotation from the official API rn, im instead going to have to get
#     the top players ranking list, then get the match history of those players (100 games) and check in which games they have not gained or lost any trophies. Those games
#     were played in the competetive mode. Then just go through maps in those games and add them to a set. after that i should have all the possible power league maps.
    path = '{}/map_list.txt'.format(settings.STATICFILES_DIRS[0])
    headers = {
        'Authorization': "Bearer: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVlN2I0NTFlLThkM2MtNDkwNC1iZGRiLTU1Mzc4MmRiOWQ3MCIsImlhdCI6MTcwODE4Mjc5Mywic3ViIjoiZGV2ZWxvcGVyLzQ5MzI1NGU4LTQ1YTQtNjViYy1hMGEyLTI3ZmM0ZjQ4NWZhZiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiODQuMjQ5LjEwLjEzMiIsIjEwOS4yMDQuMTc2LjIyIl0sInR5cGUiOiJjbGllbnQifV19.A2yGpfyPIsZxyFJDPzIw2_0oZI5kb6OZPPhwiISMUf08IYGT31Eh9_XvBpbY0ezCcZWdXRAyfBkti_TsawsCGA"
    }
    map_dict = {}

    top_players = requests.get('https://api.brawlstars.com/v1/rankings/global/players?limit=100', headers)
    top_players = top_players.json()
    top_players_tags = []
    search_response(top_players,'tag', None, top_players_tags)

    def look_for_ranked_games(game_data, map_dict):
        if not game_data['items']:
            return print("No games retrieved")
        for battles in game_data['items']:         
            if battles['battle']:
                battle_type = battles['battle']['type']      
                if battle_type == 'soloRanked' or battle_type == 'teamRanked':
                    
                    ranked_game_map = str(battles['event']['map'])
                    ranked_game_mode = str(battles['battle']['mode'])
                    if ranked_game_mode in map_dict:
                        map_dict[ranked_game_mode].add(ranked_game_map)
                    else:
                        map_dict[ranked_game_mode] = {ranked_game_map}

    for player in top_players_tags:

        player = player.replace('#', '')
        request_link = 'https://api.brawlstars.com/v1/players/%23{}/battlelog'.format(player)
        all_games = requests.get(request_link, headers)
        all_games = all_games.json()
        look_for_ranked_games(all_games, map_dict)

    def camel_case_to_normal(s):
        words = []
        start = 0
        for i, c in enumerate(s[1:], start = 1):
            if c.isupper():
                words.append(s[start:i].capitalize())
                start = i
        
        words.append(s[start:].capitalize())
        result = ' '.join(words)
        return result
    
    def save_maps(maps):

        for mode, map_set in maps.items():
            map_list = list(map_set)
            maps[mode] = map_list 
            mode = mode.replace("'","\"").replace("\"s", "'s")
            mode = camel_case_to_normal(mode)
            
            db_mode = Mode(mode_name = mode)
            db_mode.save()
            for map in map_list:
                map = map.replace("'","\"").replace("\"s", "'s")

                db_map = Map(map_name = map, mode_name= db_mode)
                
                if not Map.objects.filter(map_name= map, mode_name = db_mode).exists():
                    db_map.save()
        return 

    save_maps(map_dict)