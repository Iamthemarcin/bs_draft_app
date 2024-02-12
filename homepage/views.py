from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import requests
import os
import random
from io import BytesIO
from django.conf import settings

def index(request):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
    cookies = {
        'cookie_name': 'cookie_value'
    }
    game_modes = ['Brawl-Ball', 'Gem-Grab', 'Heist', 'Knockout', 'Wipeout', 'Hot-Zone']
    chosen_mode = random.choice(game_modes)

    path = '{}/images/brawlers/'.format(settings.STATICFILES_DIRS[0])
    img_list = os.listdir(path)
    half = len(img_list)//2
    top_row = img_list[:half]
    bottom_row = img_list[half:]
    events_request = requests.get('https://api.brawlapi.com/v1/events')
    events_json = events_request.json()
    mode_icon_link = []


    act_events_req = requests.get('https://api.brawlstars.com/v1/#/definitions/PowerPlaySeason')
    act_events = act_events_req.json()
    print(act_events)
    def print_values(data, search_word, chosen_mode):        
        if isinstance(data,dict):
            for key,value in data.items():
                if search_word == key and chosen_mode in value and 'header' not in value: #aight i tried returning it but it would require me to use the yield generator stuff and then iterate over the result??? there has to be a better way of returning it without using a list xd
                    mode_icon_link.append(value)
                    break
                if isinstance(value, dict) or isinstance(value, list):
                    print_values(value, search_word, chosen_mode)
        if isinstance(data, list):
            for i in data:
                print_values(i, search_word, chosen_mode)
    print_values(events_json, 'imageUrl', chosen_mode)
    print(mode_icon_link[0])
    chosen_mode = chosen_mode.replace('-',' ')


    # update_brawler_pics(request) #everytime you want to update the brawler run this, for now xd maybe later make this run every week or something
    context = {'top_row':top_row, 'bottom_row':bottom_row, 'mode_icon_link' : mode_icon_link[0], 'chosen_mode': chosen_mode}
    return render(request, "homepage.html", context)


#For now i just get the pics from the brawlify api whenever there's a big update
def update_brawler_pics(request):
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