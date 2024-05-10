from django.shortcuts import render
import os
import random
import json
from decimal import Decimal
from django.core import serializers
from django.conf import settings
from picks_manager.models import Map, WinRate, Brawler, WinRateSerializer, BrawlerClass
from django.db.models import F
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer

#function respoinsible for calculating which brawlers to suggest
def get_top_brawlers(map, ammount, picked_brawlers = None):
    if picked_brawlers: #adjust the picks depending on what has been already picked. classes and their counters are defined in picksmanager views. 
        team1 = set()
        team2 = set()
        for i,brawler_name in enumerate(picked_brawlers, start = 1): #determine which brawlers belong to your and enemy team depending which player is choosing the pick
            if i in [1,4,5]:
                team1.add(brawler_name)
            else:
                team2.add(brawler_name)
        if len(picked_brawlers) in [1,2,5]:
            enemy_team = team1
            players_team = team2
        else:
            enemy_team = team2
            players_team = team1
        top_brawlers = WinRate.objects.filter(map_name__map_name = map).calc_viability().order_by('-viability').exclude(brawler_name__in=picked_brawlers)[:ammount*3] ### map_name is foreign key to map object which has a map_name GET PRANKED
        #if a brawler counters enemies his viability goes up, if it gets countered it goes down.
        for brawler_name in enemy_team:
            picked_brawler = Brawler.objects.get(brawler_name = brawler_name)
            picked_brawler_class = picked_brawler.brawler_class
            for top_brawler in top_brawlers:
                top_brawler_class = top_brawler.brawler_name.brawler_class
                top_brawler_class = BrawlerClass.objects.get(class_name = top_brawler_class)
                #print(f'{top_brawler} class is {top_brawler_class} and gets countered by {top_brawler_class.countered_by}')
                if str(picked_brawler_class) in top_brawler_class.countered_by:
                    #print('On ' + str(top_brawler) + ' is countered by ' + str(picked_brawler) + ' and has ' + str(top_brawler.viability) + ' viability')
                    top_brawler.viability -= 0.15
                    #print('Its new viability is: ' + str(top_brawler.viability))
                if str(top_brawler_class) in picked_brawler_class.countered_by:
                    top_brawler.viability += 0.15

        #synergies. For example if your team has a thrower (artillery) already you never want another thrower.

        #IF SITE EVER BECOMES SLOW THIS CAN BE EASILY IMPROVED.
        for brawler_name in players_team:
            picked_brawler = Brawler.objects.get(brawler_name = brawler_name)
            picked_brawler_class = picked_brawler.brawler_class

            for top_brawler in top_brawlers:
                top_brawler_class = top_brawler.brawler_name.brawler_class
                top_brawler_class = BrawlerClass.objects.get(class_name = top_brawler_class)

                if str(picked_brawler_class) == str(top_brawler_class) == 'Artillery':
                    top_brawler.viability -= 1 
        top_brawlers = sorted(top_brawlers, key = lambda o:o.viability, reverse=True)    

    else:
        top_brawlers = WinRate.objects.filter(map_name__map_name = map).calc_viability().order_by('-viability')[:ammount]
    
    for top_brawler in top_brawlers:
        top_brawler.use_rate = round(top_brawler.use_rate * 100,2)
        top_brawler.win_rate = round(top_brawler.games_won *100/top_brawler.games_played,2)
        top_brawler.viability = round(top_brawler.viability,2)

    return top_brawlers[:16]

#renders the page
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
    chosen_map = chosen_map_obj
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
    return JsonResponse({'brawlers':serializer.data, 'map_src': chosen_map.image_url}, safe=False)

def brawler_pick(request):
    brawler_data = json.loads(request.body)['brawler_data']
    map_name = json.loads(request.body)['map_name']
    picked_brawlers = list(brawler_data.values())
    top_brawlers = get_top_brawlers(map_name, 16, picked_brawlers=picked_brawlers)
    top_brawlers_serializer = WinRateSerializer(top_brawlers, many=True)

    context = {'brawler_data': brawler_data, 'map_name': map_name, 'top_brawlers': top_brawlers_serializer.data}
    return  JsonResponse(context, safe=False)