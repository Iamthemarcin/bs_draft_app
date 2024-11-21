from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import requests
import datetime
from io import BytesIO
from django.conf import settings
from django.templatetags.static import static
from .models import Map, Mode, Player, ScannedData, Brawler, WinRate, BrawlerClass, HeadToHead


# Create your views here.

#Functions below are used to populate and manage the database from Brawlify and official Brawlstars APIs.

"""ORDER OF OPERATIONS WHEN NO ITEMS IN DB:
0. update_brawler_classes
1. get_player_tags
1. update_brawler_list
1. update_brawler_pics
1. update map list and win rates<--  repeat a couple of thousand times (set ammount_of_battlelogs).
2. update modes <- do this when icon missing
2. update map pics <- this comes from different API than battlelogs, i dont want to put more calls into wr function since i use it the most and its a clusterf already
"""


#updating what kinda modes there are in powerleague.
# the way to do it is: run the update_map_list to find all the current powerleague maps. fill the modes table with just the mode names.
# after that run update modes, to find all the icons for the modes from the different API.

class ManageDB:
    headers = {
        'Authorization': "Bearer: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjAyMmVlODU0LTJlNTUtNGViOC1hMzdkLTY4NWRmNGVmMWNmMyIsImlhdCI6MTcyNjE0NTIyNSwic3ViIjoiZGV2ZWxvcGVyLzQ5MzI1NGU4LTQ1YTQtNjViYy1hMGEyLTI3ZmM0ZjQ4NWZhZiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTU5LjIyMy4yMzQuNTkiLCI1MS4yMC44LjEiLCIxMDkuMTk3LjE4Ny42MCIsIjg0LjI0OS4xMC4xMzIiXSwidHlwZSI6ImNsaWVudCJ9XX0.or5nTEjeWa0AxZXJY2FBTbUpKky9iJ8vq3zsN-Xi-hd3VrNkmv9HwlNOmVsH2--Kr2GHaOvaLeoAgQextg1LtA"
    }
    i = 0
    curr_day = datetime.date.today()
    #function to navigate the data from brawl stars APIs, #data is json, search word is the key you look for, chosen_mode is used when you need a specific value for the key, results_list is what you store results in
    def search_response(self, data, search_word, chosen_mode, results, return_parent = False):
        if isinstance(data,dict):
            for key,value in data.items():
                #sometimes I want to check the values for stuff and sometimes i dont, this slows down the function a bit but makes it more reusable, i dont have that much data to get thru
                if chosen_mode:
                    if search_word.lower() in key.lower():
                        clean_value = value.replace('-', '').lower().replace(' ', '')
                        chosen_mode = chosen_mode.lower()
                        if chosen_mode.lower() == clean_value:
                            if return_parent:  ##sometimes i need the whole object, but only one so break it baby.
                                results['map_object'] = data
                                break

                            elif "header" not in value:
                                results.append(value)
                else:
                    if search_word == key:
                        if return_parent:
                            results.append(data)
                        else:
                            results.append(value)
                if isinstance(value, dict) or isinstance(value, list):
                    self.search_response(value, search_word, chosen_mode, results, return_parent)
        if isinstance(data, list):
            for i in data:
                self.search_response(i, search_word, chosen_mode, results, return_parent)

    def update_brawler_classes(self):      
        class_counters = {'Assassin': ['Controller', 'Tank'], 'Artillery':'Assassin', 'Controller':'Artillery', 'Marksman':'Assassin', 'Damage Dealer':'Marksman', 'Support':['Tank', 'Assassin'], 'Tank':['Damage Dealer', 'Controller']}
        
        for b_class,counters in class_counters.items():
            if isinstance(counters,list):
                for counter in counters:
                    try:
                        brawler_class = BrawlerClass.objects.get(class_name = b_class)
                    except:
                        brawler_class = BrawlerClass(class_name = b_class)

                    if counter in brawler_class.countered_by:
                        continue
                    brawler_class.countered_by += counter + ' '
                    brawler_class.save()
            else:
                    try:
                        brawler_class = BrawlerClass.objects.get(class_name = b_class)
                    except:
                        brawler_class = BrawlerClass(class_name = b_class)
                    
                    if counters not in brawler_class.countered_by:
                        brawler_class.countered_by += counters                
                        brawler_class.save()
        #crow being an (according to supercells db) assasin is very counterintuitive, he's more of a support.
        try: 
            crow = Brawler.objects.get(brawler_name = "Crow")
        except Brawler.DoesNotExist:
            self.update_brawler_list()
            crow = Brawler.objects.get(brawler_name = "Crow")
        support_class = BrawlerClass.objects.get(class_name = "Support")
        crow.brawler_class = support_class
        crow.save()
        
    @staticmethod
    def update_brawler_list():        
        #updating the brawlers properties based on api
        all_brawlers_request = requests.get('https://api.brawlapi.com/v1/brawlers')
        all_brawlers_json = all_brawlers_request.json()
        for brawler in all_brawlers_json['list']:
            brawler_name = brawler['name']
            if brawler_name == "Larry-&-Lawrie":
                brawler_name = brawler_name.replace('-', ' ')
            rarity = brawler['rarity']['name']
            image_url = brawler['imageUrl']
            brawler_class = brawler['class']['name']
            brawler_class = BrawlerClass.objects.filter(class_name = brawler_class)[0]
            brawler = Brawler(brawler_name = brawler_name, rarity = rarity, image_url = image_url, brawler_class = brawler_class)
            brawler.save()
        #updating the brawler properties based on my csv document
        
        x = static('misc/brawler_traits.csv')
        with open(f'.{x}', 'r+') as f:
            brawlers = f.read().splitlines() 

            for brawler_properties in brawlers[1:]:
                brawler_properties_list = brawler_properties.split(",")
                brawler_name = brawler_properties_list[0]
                easy_to_counter = brawler_properties_list[1]
                has_pets = brawler_properties_list[2]
                countered_by_pets = brawler_properties_list[3]
                counters_pets = brawler_properties_list[4]
                hz_sitter = brawler_properties_list[5]
                gem_carrier = brawler_properties_list[6]
                db_brawler = Brawler.objects.get(brawler_name = brawler_name)
                db_brawler.brawler_name = brawler_name
                db_brawler.easy_to_counter = easy_to_counter
                db_brawler.has_pets = has_pets
                db_brawler.countered_by_pets = countered_by_pets
                db_brawler.counters_pets = counters_pets
                db_brawler.hz_sitter = hz_sitter
                db_brawler.gem_carrier = gem_carrier
                db_brawler.save()
            f.close()


    def update_modes(self): #use this after updating maps and cleaning maps, at least 1k battlelogs. 
        bg_colors = {
            'Gem Grab':'rgba(154,61,243,255)',
            'Heist':'rgba(214,92,211,255)',
            'Bounty':'rgba(0,207,255,255)',
            'Brawl Ball':'rgba(140,160,224,255)',
            'Hot Zone':'rgba(227,59,80,255)',
            'Knockout':'rgba(247,131,28,255)',
        }
        all_my_modes = Mode.objects.all()
        all_modes_request = requests.get('https://api.brawlify.com/v1/gamemodes')
        all_modes = all_modes_request.json()

        for mode in all_my_modes:
            result = {}

            # this link for example leads to bounty 'https://cdn.brawlify.com/game-modes/regular/48000003.png'

            self.search_response(all_modes, 'name', mode.mode_name.replace(' ', ''), result, return_parent = True)
            mode.mode_icon = result['map_object']['imageUrl']
            mode.mode_color = bg_colors[mode.mode_name]
            mode.save()
    
    def update_map_pics(self):
        my_maps = Map.objects.all()
        all_maps_request = requests.get('https://api.brawlapi.com/v1/maps')
        all_maps = all_maps_request.json()
        for map in my_maps:
            clean_name = map.map_name.replace('\'', '')
            map_obj = {}
            self.search_response(all_maps, 'name', clean_name, map_obj, return_parent = True)
            image_url = map_obj['map_object']['imageUrl']
            map.image_url = image_url
            map.save()

    @staticmethod
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

    def get_player_tags(self):
        x = static('misc/country_codes')
        with open(f'.{x}', 'r+') as f:
            country_codes = f.readlines()
            country_codes_list=[]
            for country_code in country_codes[1:]:
                country_code = country_code.replace('\n', '')
                country_codes_list.append(country_code)
            f.close()
            
        for country in country_codes_list:
            top_players = requests.get(f'https://api.brawlstars.com/v1/rankings/{country}/players', self.headers)
            top_players = top_players.json()
            top_players_tags = []
            self.search_response(top_players,'tag', None, top_players_tags)

            for player_tag in top_players_tags:
                db_player_tag = Player(player_tag = player_tag)
                if not Player.objects.filter(player_tag = player_tag).exists():
                    d = datetime.datetime.today() - datetime.timedelta(days=4)
                    db_player_tag.last_checked = d
                    db_player_tag.save()
        return
    
    def update_win_rate(self,player_tag, result, teams, map):
        player_team = 1
        team_0_brawlers = []

        #find which team our player was a part of 
        for player in teams[0]:
            team_0_brawlers.append(player['brawler']['name'])
            if player['tag'] == player_tag:
                player_team = 0
        
        if result == 'victory':
            winning_team = player_team
        else: #if player team is 1 and he lost, winning team is 0. if player team is 0 and he lost, winning team is 1.
            winning_team = 1 - player_team
        
        self.update_head_to_head_scores(result, teams[winning_team], teams[1 - winning_team], map)
        for player in teams[winning_team]:
            brawler_name = player['brawler']['name']
            brawler = Brawler.objects.get_or_update(brawler_name)

            try:
                wr_obj = WinRate.objects.get(brawler_name = brawler, map_name = map)
                wr_obj.games_played += 1
                wr_obj.games_won += 1
                wr_obj.save()
            except WinRate.DoesNotExist:
                WinRate(brawler_name = brawler, map_name = map, games_played = 1, games_won = 1, use_rate = 1/map.games_played).save()
        
        for player in teams[1-winning_team]:
            brawler_name = player['brawler']['name']
            brawler = Brawler.objects.get_or_update(brawler_name)

            try:
                wr_obj = WinRate.objects.get(brawler_name = brawler, map_name = map)
                wr_obj.games_played += 1
                wr_obj.save()
            except WinRate.DoesNotExist:
                WinRate(brawler_name = brawler, map_name = map, games_played = 1, games_won = 0, use_rate = 1/map.games_played).save()
        return
    
    def update_head_to_head_scores(self, result, winning_team, losing_team, map):
        for winner in winning_team:
            winning_brawler = winner['brawler']['name']
            winning_brawler = Brawler.objects.get_or_update(winning_brawler)
            for loser in losing_team:
                losing_brawler = loser['brawler']['name']
                losing_brawler = Brawler.objects.get_or_update(losing_brawler)
                matches_won_by_a = 1
                brawlers = [winning_brawler, losing_brawler]
                if winning_brawler.brawler_name > losing_brawler.brawler_name:
                    brawlers = [losing_brawler, winning_brawler]
                    matches_won_by_a = 0
                try:
                    head_to_head = HeadToHead.objects.get(brawler_a = brawlers[0], brawler_b = brawlers[1], map = map) ###left brawler always needs to be smaller than right alphabetically
                    head_to_head.matches_played += 1
                    head_to_head.matches_won_by_a += matches_won_by_a
                    head_to_head.save()
                except:

                    head_to_head = HeadToHead(brawler_a = brawlers[0], brawler_b = brawlers[1], map = map, matches_played = 1, matches_won_by_a = matches_won_by_a)
                    head_to_head.save()


        
    
    def look_for_ranked_games(self, game_data, player, debug = False): #helper function, used in updating the winrate. 

        player_tag = player.player_tag
        if not 'items' in game_data:
            print("No games retrieved" + str(game_data))
            return 
        #check if the last game was played within last x days.
        last_game = len(game_data['items'])-1
        date = game_data['items'][last_game]['battleTime']
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        game_time = datetime.date(year = year,month = month,day = day)
        time_delta = game_time - player.last_checked
        if time_delta.days < 2 and not debug: #for debug stuff i want to check the game anyways
            print(game_time, player.last_checked, time_delta)
            return

        for battles in game_data['items']:         
            if battles['battle']:
                try:
                    battle_type = battles['battle']['type']  
                except KeyError: ####older gamemodes data have diff datastructure, just ignore it, not in ranked anyways lol.
                    continue
                if battle_type == 'soloRanked' or battle_type == 'teamRanked':  #i've seen all of these somehow
                    self.i += 1
                    if self.i % 10 == 0:
                        print(str(self.i) + " ranked games have been checked")
                    ranked_game_map = str(battles['event']['map'])
                    ranked_game_mode = str(battles['battle']['mode'])

                    #this part creates not only maps, but modes too, since they're like right here anyway, cant assign the image tho (diff api) 
                    # so gotta make another call (the update_modes function).
                    #( Wont make the call in this funciton tho, too much stuff going on already and its gon be used thousands of times to update winrate.

                    mode = ranked_game_mode.replace("'","\"").replace("\"s", "'s")
                    mode = self.camel_case_to_normal(mode)
                    try: 
                        db_mode = Mode.objects.get(mode_name = mode)
                    except Mode.DoesNotExist:
                        db_mode = Mode(mode_name = mode)
                        db_mode.save()

                    map = ranked_game_map.replace("'","\"").replace("\"s", "'s")
                    try:
                        db_map = Map.objects.get(map_name = map, mode_name= mode) 
                        db_map.games_played += 1
                        db_map.save()
                    #if map doesnt exist and there are less than the ammount of seasonal maps in db, create it, if it does add a game played to the map
                    except Map.DoesNotExist:
                        map_list = list(Map.objects.all().order_by('games_played'))

                        try:
                            ammount_of_maps = ScannedData.objects.first().ammount_of_maps
                        except AttributeError:
                            print("You need to set the ammount of maps for this season in ScannedData object. For now defaulting to 24")
                            ammount_of_maps = 24

                        if len(map_list) < ammount_of_maps:
                            db_map = Map(map_name = map, mode_name= db_mode, games_played = 1)
                            db_map.save()
                        else:
                            continue
                    #this part is for wr calcualting, wasnt planning on it being here but here we are
                    result = battles['battle']['result']
                    teams = battles['battle']['teams']
                    self.update_win_rate(player_tag, result, teams, db_map)    
        return 
                
    def camel_case_to_normal(self, s):  
        words = []
        start = 0
        for i, c in enumerate(s[1:], start = 1):
            if c.isupper():
                words.append(s[start:i].capitalize())
                start = i
        words.append(s[start:].capitalize())
        result = ' '.join(words)
        return result

    def update_map_list_and_winrate(self, ammount_of_battlelogs, debug = False): #allright, so there isnt any way to get the current power league map rotation from the official API rn, im instead going to have to get
    #     the top players ranking list, then get the match history of those players (100 games) and check in which games they have played powerleague. 
    #     Then just go through maps in those games and add them to a set. after doing that a couple of times i should have all the possible power league maps.

        
        #I only want to send ammount_of_battlelogs requests per map update call
        try:
            player_num_object = ScannedData.objects.first()
            player_num = player_num_object.last_player_checked
        except AttributeError:
            player_num_object = ScannedData(last_player_checked = 0, scanned_games = 0, ammount_of_maps = 24)
            player_num = 0

        player_ammount = Player.objects.count()
        #I dont want to update my maps based on the same players everytime (they have same battles duh), so i get a couple thousand best player tags and then go through them X at a time. If I went through all of them then go back to the beggining.
        if player_num > player_ammount - ammount_of_battlelogs:
            player_num = 0       
        
        players = Player.objects.all()[player_num:player_num+ammount_of_battlelogs]
        player_num_object.last_player_checked = player_num + ammount_of_battlelogs
        player_num_object.save()
        
        if ScannedData.objects.all().count() > 1:
            ScannedData.objects.first().delete() #im manipulating the pk here which i shouldnt do but whatever. just delete the old object

        #retrieve last games from players
        for player in players:
            player_tag = player.player_tag
            date = datetime.date.today()
            player.last_checked = date
            player.save()
            player_tag_link = player_tag.replace('#', '')
            request_link = 'https://api.brawlstars.com/v1/players/%23{}/battlelog'.format(player_tag_link)
            try: 
                all_games = requests.get(request_link, self.headers, timeout = 2)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching the game data from player {player}. Fix it one day maybe. No clue what causes it yet, setting bigger timeout helps a lot tho.")
                print(e)
                continue


            all_games = all_games.json()
            self.look_for_ranked_games(all_games, player, debug = debug)        
        
        return self.i
    
    #i could make another if statement in the update_map_list function to not add them in the first place but that place is a mess
    #and i dont want to make it execute longer. just run this after updating wr. 
class CleaningDB:    
    @staticmethod
    def clean_up_the_maps():
        max_amm_of_maps = 18 #sometimes peoples games from previous season get thru to the db, this func cleans up those games from db
        map_list = list(Map.objects.all().order_by('games_played'))
        while len(map_list) > max_amm_of_maps:
            print("Map removed: ", map_list[0].map_name)
            Map.objects.filter(map_name = map_list[0].map_name).delete()
            map_list.pop(0)
        return
    @staticmethod
    def fix_use_rate(): #userate got broken once by some divine intervention which i dont understand, cant reproduce, maybe learn how to write tests!!
        win_rate_objects = WinRate.objects.all()
        for win_rate_obj in win_rate_objects:
            db_map = Map.objects.get(map_name = win_rate_obj.map_name)
            actual_use_rate = win_rate_obj.games_played/db_map.games_played
            if win_rate_obj.use_rate != actual_use_rate:
                win_rate_obj.use_rate = actual_use_rate
                win_rate_obj.save()
        return

m = ManageDB()
c = CleaningDB()
#m.update_brawler_classes()
#m.update_brawler_list()
#m.update_brawler_pics()
#m.get_player_tags()
#m.update_map_list_and_winrate(15)
#m.update_modes()
#m.update_map_pics()

#c.clean_up_the_maps()
#c.fix_use_rate()
