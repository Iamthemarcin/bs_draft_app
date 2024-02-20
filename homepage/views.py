from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import requests
import os
import random
import json
from io import BytesIO
from django.conf import settings


#function to navigate the data from brawl stars APIs, #data is json, search word is the key you look for, chosen_mode is used when you need a specific value for the key, results_list is what you store results in
def search_response(data, search_word, chosen_mode, results_list):
    if isinstance(data,dict):
        for key,value in data.items():
            #sometimes I want to check the values for stuff and sometimes i dont, this slows down the function a bit but makes it more reusable, i dont have that much data to get thru
            if chosen_mode:
                if search_word.lower() == key.lower():
                    clean_value = value.replace('-', '')
                    print(chosen_mode, ' ', clean_value)
                    if chosen_mode.lower() in clean_value.lower() and 'header' not in value:
                        results_list.append(value)
            else:
                if search_word == key:
                    results_list.append(value)
            if isinstance(value, dict) or isinstance(value, list):
                search_response(value, search_word, chosen_mode, results_list)
    if isinstance(data, list):
        for i in data:
            search_response(i, search_word, chosen_mode, results_list)

def update_map_list(): #allright, so there isnt any way to get the current power league map rotation from the official API rn, im instead going to have to get
#     the top players ranking list, then get the match history of those players (100 games) and check in which games they have not gained or lost any trophies. Those games
#     were played in the competetive mode. Then just go through maps in those games and add them to a set. after that i should have all the possible power league maps.
    path = '{}/map_list.txt'.format(settings.STATICFILES_DIRS[0])
    headers = {
        'Authorization': "Bearer: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVlN2I0NTFlLThkM2MtNDkwNC1iZGRiLTU1Mzc4MmRiOWQ3MCIsImlhdCI6MTcwODE4Mjc5Mywic3ViIjoiZGV2ZWxvcGVyLzQ5MzI1NGU4LTQ1YTQtNjViYy1hMGEyLTI3ZmM0ZjQ4NWZhZiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiODQuMjQ5LjEwLjEzMiIsIjEwOS4yMDQuMTc2LjIyIl0sInR5cGUiOiJjbGllbnQifV19.A2yGpfyPIsZxyFJDPzIw2_0oZI5kb6OZPPhwiISMUf08IYGT31Eh9_XvBpbY0ezCcZWdXRAyfBkti_TsawsCGA"
    }
    map_dict = {}

    top_players = requests.get('https://api.brawlstars.com/v1/rankings/global/players?limit=50', headers)
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

    def clean_up_the_maps(maps):
        for key, value in maps.items():
            value = list(value)
            maps[key] = value

        maps = str(maps)
        clean_map_dict = maps.replace("'","\"").replace("\"s", "'s")
        return clean_map_dict

    map_dict = clean_up_the_maps(map_dict)
    map_list = open(path, 'w')
    map_list.write('{}'.format(map_dict))
    map_list.close()

def index(request):
    #whenever a power league update comes use this function XD
    #update_map_list()  

    path = '{}/images/brawlers/'.format(settings.STATICFILES_DIRS[0])
    map_path = '{}/map_list.txt'.format(settings.STATICFILES_DIRS[0])
    img_list = os.listdir(path)
    half = len(img_list)//2
    top_row = img_list[:half]
    bottom_row = img_list[half:]
    gamemodes_request = requests.get('https://api.brawlapi.com/v1/gamemodes')
    gamemodes_json = gamemodes_request.json()    
    #choose a random map and mode

    with(open(map_path, 'r')) as map_dict_txt:
        map_dict_str = map_dict_txt.read().rstrip('\n')
    map_dict_txt.close()
    map_dict = json.loads(map_dict_str)
    random_mode = random.sample(map_dict.keys(), 1)[0]
    chosen_map = random.sample(map_dict[random_mode],1)[0]
    mode_icon_link = []

    # find the icon for the gamemode, could also just make a list and save them locally every season,not sure, ill put it in a function in case i wanna do that.
    search_response(gamemodes_json, 'imageUrl', random_mode, mode_icon_link)
    
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
    chosen_mode = camel_case_to_normal(random_mode)

 
    print(mode_icon_link)
    # update_brawler_pics(request) # <----- everytime you want to update the brawler run this, for now xd maybe later make this run every week or something
    context = {'top_row':top_row, 'bottom_row':bottom_row, 'mode_icon_link' : mode_icon_link[0], 'chosen_mode': chosen_mode, 'chosen_map': chosen_map }
    return render(request, "homepage.html", context)


#For now i just get the pics from the brawlify api whenever there's a big update
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