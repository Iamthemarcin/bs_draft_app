from django.test import TestCase
from picks_manager.views import ManageDB
from picks_manager.models import Player, WinRate, Map, HeadToHead, Brawler, Synergy, BrawlerClass
from functools import wraps
import requests
import datetime
import time
import asyncio

# Create your tests here.


def timer(func):
    """helper function to time functions"""

    @wraps(func)  # used for copying func metadata
    def wrapper(*args, **kwargs):
        # record start time
        start = time.time()

        # func execution
        result = func(*args, **kwargs)

        duration = (time.time() - start) * 1000
        # output execution time to console
        print('view {} takes {:.2f} ms'.format(
            func.__name__,
            duration
        ))
        return result
    return wrapper


class TestWinRatesCollection(TestCase):

    @classmethod
    def setUpTestData(cls):
        """This method is run once for the whole test class."""
        last_checked = datetime.date.today() - datetime.timedelta(days=3)
        cls.db_player_tag = Player.objects.create(
            player_tag="#PU00QLLV0", last_checked=last_checked)
        m = ManageDB()
        m.update_brawler_classes()
        m.update_brawler_list()
        m.look_for_ranked_games(
            example_piece_of_response_data, cls.db_player_tag, debug=True)
        print("The database is ready")

    def test_ammount_of_wr_data(self):  # there should be 6 brawlers each game
        wr_objects = WinRate.objects.all()
        ammount_of_wr_data = 0
        for wr in wr_objects:
            ammount_of_wr_data += wr.games_played
        self.assertEqual(ammount_of_wr_data, 12)

    def test_use_rate(self):
        win_rate_objects = WinRate.objects.all()
        for win_rate_obj in win_rate_objects:
            db_map = Map.objects.get(map_name=win_rate_obj.map_name)
            actual_use_rate = win_rate_obj.games_played/db_map.games_played
            self.assertEqual(actual_use_rate, win_rate_obj.use_rate)

    def test_get_brawler(self):
        brawler = Brawler.objects.get_or_update(brawler_name="Tick")
        self.assertEqual(brawler.brawler_name, "Tick")

    def test_head_to_head(self):
        brawler_a = Brawler.objects.get_or_update(brawler_name="Kenji")
        brawler_b = Brawler.objects.get_or_update(brawler_name="Tick")
        myh2h = HeadToHead.objects.get(
            brawler_a=brawler_a, brawler_b=brawler_b)
        self.assertEqual(myh2h.matches_won_by_a, 2)

    def test_synergies(self):
        winning_team = [{'tag': '#PU00QLLV0', 'name': 'ズラタンイブラヒモビッチ', 'brawler': {'id': 16000085, 'name': 'KENJI', 'power': 11, 'trophies': 1014}}, {'tag': '#2Y9QRCQL', 'name': '겨링겨링', 'brawler': {'id': 16000084, 'name': 'MOE', 'power': 11, 'trophies': 1030}}, {'tag': '#8CL998GVY', 'name': 'みず💧', 'brawler': {'id': 16000038, 'name': 'PAM', 'power': 11, 'trophies': 925}}]
        losing_team = [{'tag': '#PRQULYG9J', 'name': 'Thə Łúcifer惡😈', 'brawler': {'id': 16000025, 'name': 'TICK', 'power': 11, 'trophies': 991}}, {'tag': '#YYYYJUP9', 'name': '鬥士', 'brawler': {'id': 16000085, 'name': 'EDGAR', 'power': 11, 'trophies': 1029}}, {'tag': '#P2L2LUVPV', 'name': 'Q娃', 'brawler': {'id': 16000020, 'name': 'FRANK', 'power': 11, 'trophies': 1011}}]
        db_map = Map.objects.first()
        ManageDB().update_synergies(winning_team, losing_team, db_map)
        # alphabetical order, brawler a < brawler b
        brawler_a = Brawler.objects.get_or_update(brawler_name="Moe")
        brawler_b = Brawler.objects.get_or_update(brawler_name="Pam")
        my_synergy = Synergy.objects.get(
            brawler_a=brawler_a, brawler_b=brawler_b, map=db_map)
        self.assertEqual(my_synergy.brawler_a, brawler_a)

    @timer
    def test_updating_the_database(self):
        ManageDB().update_map_list_and_winrate(50, debug = True)

    def test_fetching_player_data(self):
        m = ManageDB()
        top_players = requests.get(
            f'https://api.brawlstars.com/v1/rankings/PL/players', m.headers)

        top_players = top_players.json()
        top_players_tags = []
        m.search_response(top_players, 'tag', None, top_players_tags)

        for player_tag in top_players_tags:
            db_player_tag = Player(player_tag=player_tag)
            if not Player.objects.filter(player_tag=player_tag).exists():
                d = datetime.datetime.today() - datetime.timedelta(days=4)
                db_player_tag.last_checked = d
                db_player_tag.save()
        # gotta convert this to a list since django all objects are lazy, so iterating over em will break async
        players = list(Player.objects.all()[0:25])
        results = asyncio.run(m.fetch_all_players_data(players))
        self.assertTrue(results)

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
                "type": "soloRanked",
                "result": "victory",
                "duration": 145,
                "trophyChange": 6,
                "starPlayer": {
                    "tag": "#8CL998GVY",
                    "name": "みず💧",
                    "brawler": {
                        "id": 16000038,
                        "name": "PAM",
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
                                "name": "PAM",
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
                                "name": "TICK",
                                "power": 11,
                                "trophies": 991
                            }
                        },
                        {
                            "tag": "#YYYYJUP9",
                            "name": "鬥士",
                            "brawler": {
                                "id": 16000085,
                                "name": "EDGAR",
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
        },
        {
            "battleTime": "20241022T052147.000Z",
            "event": {
                "id": 15000763,
                "mode": "brawlBall",
                "map": "Offside Trap"
            },
            "battle": {
                "mode": "brawlBall",
                "type": "soloRanked",
                "result": "victory",
                "duration": 145,
                "trophyChange": 6,
                "starPlayer": {
                    "tag": "#8CL998GVY",
                    "name": "みず💧",
                    "brawler": {
                        "id": 16000038,
                        "name": "PAM",
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
                                "name": "PAM",
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
                                "name": "TICK",
                                "power": 11,
                                "trophies": 991
                            }
                        },
                        {
                            "tag": "#YYYYJUP9",
                            "name": "鬥士",
                            "brawler": {
                                "id": 16000085,
                                "name": "EDGAR",
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
