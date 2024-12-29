from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import os
import random
import json
from django.conf import settings
from picks_manager.models import Map, WinRate, Brawler, WinRateSerializer, BrawlerClass, HeadToHead
from django.http import JsonResponse
from picks_manager.views import ManageDB


def check_counterability_and_pick_rate(top_brawlers, picked_brawlers=None):
    # if the draft phase is in the early stages you should not pick brawlers that are easily counterable.
    # the base classes don't really do a good job of showing which ones would fit here so I made a custom
    # field by just assigning easy_to_counter based on my feel/experience
    if not picked_brawlers or len(picked_brawlers) < 4:
        for top_brawler in top_brawlers:

            # brawlers with super low pick rate are unfairly favoured because ppl who play them usually
            # know what they're doing and a general player will do much worse than those guys.
            use_rate = top_brawler.use_rate * 100
            if use_rate < 5:
                # in %. when pick rate is 0 viability goes down by 0.25. When its around 5% it
                # goes down by 0
                top_brawler.viability -= (0.05*use_rate + 0.25)

            easy_to_counter = str(top_brawler.brawler_name.easy_to_counter)
            if easy_to_counter == "Yes":
                top_brawler.viability -= 1

            if easy_to_counter == "Sorta":
                top_brawler.viability -= 0.5
    return top_brawlers
# func to find out if you already have a viable gem carrier in ur team


def gem_grab_update_viability(top_brawlers, gem_carriers=0):
    for top_brawler in top_brawlers:
        top_brawler_obj = top_brawler.brawler_name
        if gem_carriers < 1:
            if top_brawler_obj.gem_carrier == "Yes":
                top_brawler.viability += 0.5
            elif top_brawler_obj.gem_carrier == "Sorta":
                top_brawler.viability += 0.25
        elif gem_carriers >= 1:
            if top_brawler_obj.gem_carrier == "Yes":
                top_brawler.viability -= 0.5
            elif top_brawler_obj.gem_carrier == "Sorta":
                top_brawler.viability -= 0.25

# this function and the gem_grab function could be combined into one by just passing the mode name
# into the function and writing a tuple of variables but this feels nicer to debug
# hot zone stuff, you want at least one hot zone sitter, two are cool too.


def hot_zone_update_viability(top_brawlers, hz_sitters=0):
    for top_brawler in top_brawlers:
        top_brawler_obj = top_brawler.brawler_name
        if hz_sitters < 1:
            if top_brawler_obj.hz_sitter == "Yes":
                top_brawler.viability += 0.5
            elif top_brawler_obj.hz_sitter == "Sorta":
                top_brawler.viability += 0.25
        elif hz_sitters >= 1:
            if top_brawler_obj.hz_sitter == "Yes":
                top_brawler.viability -= 0.5
            elif top_brawler_obj.hz_sitter == "Sorta":
                top_brawler.viability -= 0.25


def divide_into_teams(picked_brawlers):
    """Divide the picked brawlers into two teams"""

    team1 = set()
    team2 = set()
    # determine which brawlers belong to your and enemy team depending which player is choosing the pick
    for i, brawler_name in enumerate(picked_brawlers, start=1):
        # The pick order is like this:
        # 1. team1
        # 2,3.team2
        # 4,5. team1
        # 6. team2
        if i in [1, 4, 5]:
            team1.add(brawler_name)
        else:
            team2.add(brawler_name)
    if len(picked_brawlers) in [1, 2, 5]:
        enemy_team = team1
        players_team = team2
    else:
        enemy_team = team2
        players_team = team1
    return players_team, enemy_team

# function respoinsible for calculating which brawlers to suggest
def get_top_brawlers(map, ammount, picked_brawlers=None):
    curr_map = Map.objects.get(map_name=map)
    curr_map_mode = str(curr_map.mode_name)

    if picked_brawlers:  # adjust the picks depending on what has been already picked. classes and their counters are defined in picksmanager views.
        players_team, enemy_team = divide_into_teams(picked_brawlers)
        top_brawlers = WinRate.objects.filter(map_name__map_name=map).calc_viability().order_by('-viability').exclude(
            brawler_name__in=picked_brawlers)[:ammount*3]  # map_name is foreign key to map object which has a map_name attr GET PRANKED myself
        # What I need here is all head to heads with correct map, where
        check_counterability_and_pick_rate(top_brawlers, picked_brawlers)

        # if a brawler class counters enemies class his viability goes up, if it gets countered it goes down.
        # similarly if a brawler has pets, his viability goes up or down depending if pets are good vs enemy brawlers.
        for brawler_name in enemy_team:
            picked_brawler = Brawler.objects.get(brawler_name=brawler_name)
            picked_brawler_class = picked_brawler.brawler_class
            has_pets = picked_brawler.has_pets
            for top_brawler in top_brawlers:
                counters_pets = top_brawler.brawler_name.counters_pets
                countered_by_pets = top_brawler.brawler_name.countered_by_pets

                # if enemy brawler has pets and top brawler is good into pets, his viability goes up
                if has_pets == "Yes":
                    if counters_pets == "Yes":
                        top_brawler.viability += 0.5
                    elif counters_pets == "Sorta":
                        top_brawler.viability += 0.25
                elif has_pets == "Sorta":
                    if counters_pets == "Yes":
                        top_brawler.viability += 0.25
                    elif counters_pets == "Sorta":
                        top_brawler.viability += 0.15

                # if enemy brawler has pets and top brawler is bad into pets, his viability goes down
                if countered_by_pets == "Yes":
                    if has_pets == "Yes":
                        top_brawler.viability -= 0.5
                    if has_pets == "Sorta":
                        top_brawler.viability -= 0.25
                elif countered_by_pets == "Sorta":
                    if has_pets == "Yes":
                        top_brawler.viability -= 0.25
                    elif has_pets == "Sorta":
                        top_brawler.viability -= 0.15

                # the section responsible for classes and their counters.
                top_brawler_class = top_brawler.brawler_name.brawler_class
                top_brawler_class = BrawlerClass.objects.get(
                    class_name=top_brawler_class)
                # print(f'{top_brawler} class is {top_brawler_class} and gets countered by {top_brawler_class.countered_by}')
                if str(picked_brawler_class) in top_brawler_class.countered_by:
                    # print('On ' + str(top_brawler) + ' is countered by ' + str(picked_brawler) + ' and has ' + str(top_brawler.viability) + ' viability')
                    top_brawler.viability -= 0.15
                    # print('Its new viability is: ' + str(top_brawler.viability))
                if str(top_brawler_class) in picked_brawler_class.countered_by:
                    top_brawler.viability += 0.15

        # synergies. For example if your team has a thrower (artillery) already you never want another thrower.

        # gem grab stuff. You want to have one real gem carrier or two pseudo carriers
        if curr_map_mode == "Gem Grab":
            gem_carriers = 0
            for brawler_name in players_team:
                picked_brawler = Brawler.objects.get(brawler_name=brawler_name)
                if picked_brawler.gem_carrier == "Yes":
                    gem_carriers += 1
                elif picked_brawler.gem_carrier == "Sorta":
                    gem_carriers += 0.5
            gem_grab_update_viability(top_brawlers, gem_carriers)

        # hot zone stuff, you want at least one hot zone sitter, two are cool too.
        if curr_map_mode == "Hot Zone":
            hz_sitters = 0
            for brawler_name in players_team:
                picked_brawler = Brawler.objects.get(brawler_name=brawler_name)
                if picked_brawler.hz_sitter == "Yes":
                    hz_sitters += 1
                elif picked_brawler.hz_sitter == "Sorta":
                    hz_sitters += 0.5
            hot_zone_update_viability(top_brawlers, hz_sitters)

        for brawler_name in players_team:
            picked_brawler = Brawler.objects.get(brawler_name=brawler_name)
            picked_brawler_class = picked_brawler.brawler_class

            for top_brawler in top_brawlers:
                top_brawler_class = top_brawler.brawler_name.brawler_class
                top_brawler_class = BrawlerClass.objects.get(
                    class_name=top_brawler_class)
                if str(picked_brawler_class) == str(top_brawler_class) == 'Artillery':
                    top_brawler.viability -= 99

        top_brawlers = sorted(
            top_brawlers, key=lambda o: o.viability, reverse=True)

    else:
        top_brawlers = WinRate.objects.filter(
            map_name__map_name=map).calc_viability().order_by('-viability')[:ammount]
        check_counterability_and_pick_rate(top_brawlers, picked_brawlers)
        if curr_map_mode == "Gem Grab":
            gem_grab_update_viability(top_brawlers)
        top_brawlers = sorted(
            top_brawlers, key=lambda o: o.viability, reverse=True)

    for top_brawler in top_brawlers:
        top_brawler.use_rate = round(top_brawler.use_rate * 100, 2)
        top_brawler.win_rate = round(
            top_brawler.games_won * 100/top_brawler.games_played, 2)
        top_brawler.viability = round(top_brawler.viability, 2)

    return top_brawlers[:16]


def calculate_counter_score(win_rate,head_to_heads):
    """Calculate counter score for every pre selected top brawler based on picked enemy brawlers"""


    pass

def get_top_brawlers_regression(map, ammount, picked_brawlers = None):
    curr_map = Map.objects.get(map_name=map)
    curr_map_mode = str(curr_map.mode_name)
    all_brawlers = {b.brawler_name.lower(): b for b in Brawler.objects.all()}

    if not picked_brawlers:
        top_brawlers = WinRate.objects.filter(
            map_name__map_name=map).calc_viability().order_by('-viability')[:ammount]
        check_counterability_and_pick_rate(top_brawlers, picked_brawlers)
        if curr_map_mode == "Gem Grab":
            gem_grab_update_viability(top_brawlers)
        top_brawlers = sorted(
            top_brawlers, key=lambda o: o.viability, reverse=True)
    else:
        players_team, enemy_team = divide_into_teams(picked_brawlers)
        top_brawlers = WinRate.objects.filter(map_name__map_name=map).calc_viability().order_by('-viability').exclude(
            brawler_name__in=picked_brawlers)[:ammount*3]  # map_name is foreign key to map object which has a map_name attr GET PRANKED myself
        # What I need here is all head to heads with correct map, where
        for top_brawler in top_brawlers:
            pairs = []
            for enemy_brawler in enemy_team:
                pairs.append([top_brawler.brawler_name,enemy_brawler].sort())
            print(pairs)
            h2h = HeadToHead.objects.filter()
            calculate_counter_score(top_brawler, 15)

    for top_brawler in top_brawlers:
        top_brawler.use_rate = round(top_brawler.use_rate * 100, 2)
        top_brawler.win_rate = round(
            top_brawler.games_won * 100/top_brawler.games_played, 2)
        top_brawler.viability = round(top_brawler.viability, 2)

    #calculate_counter_score(WinRate, HeadToHeads)
    pass
# renders the page

def index(request):
    # this is here so i can trigger stuff from picksmanager views manually when debugging.
    path = '{}/images/brawlers/'.format(settings.STATICFILES_DIRS[0])
    img_list = os.listdir(path)
    half = len(img_list)//2
    top_row = img_list[:half]
    bottom_row = img_list[half:]
    # choose a random map and mode
    all_maps = Map.objects.all().order_by('mode_name')
    maps = list(all_maps)
    maps_per_column = len(maps)/6
    columns = [i for i in range(int(len(maps)/3))]
    chosen_map_obj = random.choice(maps)
    chosen_mode = chosen_map_obj.mode_name
    chosen_map = chosen_map_obj
    mode_icon_link = chosen_map_obj.mode_name.mode_icon
    map_icon_link = chosen_map_obj.image_url
    val = URLValidator()
    try:
        val(map_icon_link)
    except ValidationError:
        ManageDB().update_map_pics()

    # choose the 16 brawlers most suitable for the map. viability is calculated by multiplying winrate and userate on the current map
    top_brawlers = get_top_brawlers(chosen_map, 16)
    top_brawlers_regression = get_top_brawlers_regression(chosen_map, 16)
    context = {'top_row': top_row, 'bottom_row': bottom_row, 'mode_icon_link': mode_icon_link, 'maps': maps,
               'chosen_mode': chosen_mode, 'chosen_map': chosen_map, 'top_brawlers': top_brawlers, 'maps_per_column': maps_per_column,
               'columns': columns}
    return render(request, "homepage.html", context)


def map_change(request):
    new_map = json.loads(request.body)['map_name']
    chosen_map = Map.objects.get(map_name=new_map)
    val = URLValidator()
    try:
        val(chosen_map.image_url)
    except ValidationError:
        ManageDB().update_map_pics()

    top_brawlers = get_top_brawlers(chosen_map.map_name, 16)
    top_brawlers_regression = get_top_brawlers_regression(chosen_map, 16)

    serializer = WinRateSerializer(top_brawlers, many=True)
    return JsonResponse({'brawlers': serializer.data, 'map_src': chosen_map.image_url}, safe=False)


def brawler_pick(request):
    brawler_data = json.loads(request.body)['brawler_data']
    map_name = json.loads(request.body)['map_name']
    picked_brawlers = list(brawler_data.values())
    top_brawlers = get_top_brawlers(
        map_name, 16, picked_brawlers=picked_brawlers)
    top_brawlers_regression = get_top_brawlers_regression(map_name, 16, picked_brawlers=picked_brawlers)

    top_brawlers_serializer = WinRateSerializer(top_brawlers, many=True)

    context = {'brawler_data': brawler_data, 'map_name': map_name,
               'top_brawlers': top_brawlers_serializer.data}
    return JsonResponse(context, safe=False)
