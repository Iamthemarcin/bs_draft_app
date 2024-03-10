from django.shortcuts import render
import os
import random
from django.conf import settings
from picks_manager.models import Map, WinRate
from django.db.models import F


def index(request):

    path = '{}/images/brawlers/'.format(settings.STATICFILES_DIRS[0])
    img_list = os.listdir(path)
    half = len(img_list)//2
    top_row = img_list[:half]
    bottom_row = img_list[half:]
    #choose a random map and mode
    maps = list(Map.objects.all())
    chosen_map_obj = random.choice(maps)
    chosen_mode = chosen_map_obj.mode_name
    chosen_map = chosen_map_obj.map_name
    mode_icon_link = chosen_map_obj.mode_name.mode_icon
    top_brawlers = WinRate.objects.filter(map_name__map_name = chosen_map).calc_viability().order_by('viability')[:12] ### TODO whenever i made the map_name field i was stupid and its confusing change it to map since its foreign key jeez
    top_brawler = top_brawlers[0]
    context = {'top_row':top_row, 'bottom_row':bottom_row, 'mode_icon_link' : mode_icon_link, 'chosen_mode': chosen_mode, 'chosen_map': chosen_map }
    return render(request, "homepage.html", context)


#For now i just get the pics from the brawlify api whenever there's a big update
