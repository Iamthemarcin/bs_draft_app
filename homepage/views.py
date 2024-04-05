from django.shortcuts import render
import os
import random
import json
from decimal import Decimal
from django.core import serializers
from django.conf import settings
from picks_manager.models import Map, WinRate, Brawler, WinRateSerializer
from django.db.models import F
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer


def get_top_brawlers(map, ammount, excluded_brawlers = None):
    if excluded_brawlers:
        top_brawlers = WinRate.objects.filter(map_name__map_name = map).calc_viability().order_by('-viability').exclude(brawler_name__in=excluded_brawlers)[:ammount] ### map_name is foreign key GET PRANKED
    else:
        top_brawlers = WinRate.objects.filter(map_name__map_name = map).calc_viability().order_by('-viability')[:ammount]
    
    
    for top_brawler in top_brawlers:
        top_brawler.use_rate = round(top_brawler.use_rate * 100,2)
        top_brawler.win_rate = round(top_brawler.games_won *100/top_brawler.games_played,2)
        top_brawler.viability = round(top_brawler.viability * 100,2)

    return top_brawlers

def index(request):
    path = '{}/images/brawlers/'.format(settings.STATICFILES_DIRS[0])
    img_list = os.listdir(path)
    half = len(img_list)//2
    top_row = img_list[:half]
    bottom_row = img_list[half:]
    #choose a random map and mode
    all_maps = Map.objects.all().order_by('mode_name')
    maps = list(all_maps)
    chosen_map_obj = random.choice(maps)
    chosen_mode = chosen_map_obj.mode_name
    chosen_map = chosen_map_obj.map_name
    mode_icon_link = chosen_map_obj.mode_name.mode_icon
    #choose the 16 brawlers most suitable for the map. viability is calculated by multiplying winrate and userate on the current map
    top_brawlers = get_top_brawlers(chosen_map,16)

    context = {'top_row':top_row, 'bottom_row':bottom_row, 'mode_icon_link' : mode_icon_link, 'maps': maps, 'chosen_mode': chosen_mode, 'chosen_map': chosen_map, 'top_brawlers': top_brawlers }
    return render(request, "homepage.html", context)


def map_change(request):
    new_map = json.loads(request.body)['map_name']
    chosen_map = Map.objects.get(map_name = new_map)
    top_brawlers = get_top_brawlers(chosen_map.map_name, 16)
    serializer = WinRateSerializer(top_brawlers, many=True)
    return JsonResponse(serializer.data, safe=False)

def brawler_pick(request):
    brawler_data = json.loads(request.body)['brawler_data']
    map_name = json.loads(request.body)['map_name']
    excluded_brawlers = list(brawler_data.values())
    top_brawlers = get_top_brawlers(map_name, 16, excluded_brawlers=excluded_brawlers)
    top_brawlers_serializer = WinRateSerializer(top_brawlers, many=True)

    context = {'brawler_data': brawler_data, 'map_name': map_name, 'top_brawlers': top_brawlers_serializer.data}
    return  JsonResponse(context, safe=False)