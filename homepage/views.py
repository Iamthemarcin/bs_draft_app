from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import requests
import os
from io import BytesIO
from django.conf import settings


# Create your views here.


def index(request):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
    cookies = {
        'cookie_name': 'cookie_value'
    }
    path = '{}/images/brawlers/'.format(settings.STATICFILES_DIRS[0])
    img_list = os.listdir(path)
    half = len(img_list)//2
    top_row = img_list[:half]
    bottom_row = img_list[half:]
    events_request = requests.get('https://api.brawlapi.com/v1/events')
    events_json = events_request.json()
    gamemode_icons = []
    def print_values(data, search_word):
        if isinstance(data,dict):
            for key,value in data.items():
                if search_word == key and 'gamemode' in value and value not in gamemode_icons:
                    gamemode_icons.append(value)
                if isinstance(value, dict) or isinstance(value, list):
                    print_values(value, search_word)
        if isinstance(data, list):
            for i in data:
                print_values(i, search_word)
    print_values(events_json, 'imageUrl')
    # update_brawler_pics(request)
    context = {'top_row':top_row, 'bottom_row':bottom_row}
    return render(request, "homepage.html", context)

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