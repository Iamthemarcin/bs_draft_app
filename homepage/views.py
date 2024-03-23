from django.shortcuts import render
import os
import random
from decimal import Decimal
from django.conf import settings
from picks_manager.models import Map, WinRate, Mode
from django.db.models import F


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
    #choose the 12 brawlers most suitable for the map. viability is calculated by multiplying winrate and userate on the current map
    top_brawlers = WinRate.objects.filter(map_name__map_name = chosen_map).calc_viability().order_by('-viability')[:16] ### TODO whenever i made the map_name field i was stupid and its confusing change it to map since its foreign key jeez
    for top_brawler in top_brawlers:
        top_brawler.use_rate = round(top_brawler.use_rate * 100,2)
        top_brawler.win_rate = round(top_brawler.games_won *100/top_brawler.games_played,2)
        top_brawler.viability = round(top_brawler.viability * 100,2)

    context = {'top_row':top_row, 'bottom_row':bottom_row, 'mode_icon_link' : mode_icon_link, 'maps': maps, 'chosen_mode': chosen_mode, 'chosen_map': chosen_map, 'top_brawlers': top_brawlers }
    return render(request, "homepage.html", context)


#For now i just get the pics from the brawlify api whenever there's a big update
