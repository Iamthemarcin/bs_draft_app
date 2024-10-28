from django.test import TestCase
from picks_manager.views import ManageDB 
from picks_manager.models import Player, WinRate, Map, BrawlerClass
import datetime 

# Create your tests here.

class TestWinRatesCollection(TestCase):

    def prepare_database(self):
        last_checked = datetime.date.today()- datetime.timedelta(days=3)
        db_player_tag = Player(player_tag = "#PU00QLLV0", last_checked = last_checked)
        db_player_tag.save()
        m = ManageDB()
        m.update_brawler_classes()
        brawler_class = BrawlerClass.objects.get(class_name = "Assassin")
        print(brawler_class)
        m.update_brawler_list()

        m.look_for_ranked_games(example_piece_of_response_data, db_player_tag, debug = True) #actual debug function, previous ones just make the db
        return print("The database is ready for testing testing 1 2 3")

    def test_num_of_scanned_brawlers(self): #there should be 6 brawlers each game
        self.prepare_database()
        wr_objects = WinRate.objects.all()
        num_of_scanned_brawlers = 0
        for wr in wr_objects:
            num_of_scanned_brawlers += wr.games_played
        self.assertEqual(num_of_scanned_brawlers, 6)
    
    def test_use_rate(self):
        win_rate_objects = WinRate.objects.all()
        for win_rate_obj in win_rate_objects:
            db_map = Map.objects.get(map_name = win_rate_obj.map_name)
            actual_use_rate = win_rate_obj.games_played/db_map.games_played
            self.assertEqual(actual_use_rate, win_rate_obj.use_rate)
        



example_piece_of_response_data = {
  "items": [
    {
      "battleTime": "20241022T052147.000Z",
      "event": {
        "id": 15000763,
        "mode": "brawlBall",
        "map": "Offside Trap"
      },
      "battle": {
        "mode": "brawlBall",
        "type": "ranked",
        "result": "victory",
        "duration": 145,
        "trophyChange": 6,
        "starPlayer": {
          "tag": "#8CL998GVY",
          "name": "みず💧",
          "brawler": {
            "id": 16000038,
            "name": "SURGE",
            "power": 11,
            "trophies": 925
          }
        },
        "teams": [
          [
            {
              "tag": "#PU00QLLV0",
              "name": "ズラタンイブラヒモビッチ",
              "brawler": {
                "id": 16000085,
                "name": "KENJI",
                "power": 11,
                "trophies": 1014
              }
            },
            {
              "tag": "#2Y9QRCQL",
              "name": "겨링겨링",
              "brawler": {
                "id": 16000084,
                "name": "MOE",
                "power": 11,
                "trophies": 1030
              }
            },
            {
              "tag": "#8CL998GVY",
              "name": "みず💧",
              "brawler": {
                "id": 16000038,
                "name": "SURGE",
                "power": 11,
                "trophies": 925
              }
            }
          ],
          [
            {
              "tag": "#PRQULYG9J",
              "name": "Thə Łúcifer惡😈",
              "brawler": {
                "id": 16000025,
                "name": "CARL",
                "power": 11,
                "trophies": 991
              }
            },
            {
              "tag": "#YYYYJUP9",
              "name": "鬥士",
              "brawler": {
                "id": 16000085,
                "name": "KENJI",
                "power": 11,
                "trophies": 1029
              }
            },
            {
              "tag": "#P2L2LUVPV",
              "name": "Q娃",
              "brawler": {
                "id": 16000020,
                "name": "FRANK",
                "power": 11,
                "trophies": 1011
              }
            }
          ]
        ]
      }
    }
  ]
}
