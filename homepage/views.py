from django.shortcuts import render
import requests
import os
import random
import json
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
    chosen_mode = random.sample(map_dict.keys(), 1)[0]
    chosen_map = random.sample(map_dict[chosen_mode],1)[0]
    mode_icon_link = []

    # find the icon for the gamemode, could also just make a list and save them locally every season,not sure, ill put it in a function in case i wanna do that.
    search_response(gamemodes_json, 'imageUrl', chosen_mode, mode_icon_link)

    print(mode_icon_link)
    # update_brawler_pics(request) # <----- everytime you want to update the brawler run this, for now xd maybe later make this run every week or something
    context = {'top_row':top_row, 'bottom_row':bottom_row, 'mode_icon_link' : mode_icon_link[0], 'chosen_mode': chosen_mode, 'chosen_map': chosen_map }
    return render(request, "homepage.html", context)


#For now i just get the pics from the brawlify api whenever there's a big update
