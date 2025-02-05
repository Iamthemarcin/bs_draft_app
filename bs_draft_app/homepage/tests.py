from django.test import TestCase
from picks_manager.models import Map, Brawler, WinRate
from homepage.views import get_top_brawlers, get_top_brawlers_regression, calculate_counter_score, calculate_synergy_score
from picks_manager.views import ManageDB
import os
import subprocess
import os

class MainLogicTest(TestCase):
    """These tests require lots of data to be of any use, make sure the functions don't alter the data in any way."""

    fixture_dir = 'fixtures/'
    fixture_dir = os.fsencode(fixture_dir)
    fixtures = []
    for file in os.listdir(fixture_dir):
        filename = os.fsdecode(file)
        # No need for player data here
        if filename == 'player_fixture.json':
            continue
        fixtures.append(filename)

    def test_get_top_brawlers_regression(self):
        my_map = Map.objects.first()
        get_top_brawlers_regression(my_map, 48)

    def test_brawler_counterability(self):
        brawler = WinRate.objects.get(brawler_name = "Sprout", map_name__map_name = "Flaring Phoenix")
        ManageDB().update_brawlers_counterability(brawler)
        self.assertLessEqual(brawler.counterability, 1.0)
        self.assertGreaterEqual(brawler.counterability, 0.0)

    def test_synergy_score_calculation(self):
        top_brawler = WinRate.objects.get(brawler_name = 'Sprout', map_name__map_name = "Flaring Phoenix")
        players_team = ["Piper", "Fang"]
        curr_map = Map.objects.get(map_name = "Flaring Phoenix")
        synergy_score = calculate_synergy_score(top_brawler, players_team, curr_map)
        self.assertGreaterEqual(synergy_score, 0.0)
        self.assertLessEqual(synergy_score, 1,0)

    def test_counter_score_calculation(self):
        top_brawler = WinRate.objects.get(brawler_name = 'Sprout', map_name__map_name = "Flaring Phoenix")
        enemy_team = ["Mortis", "Fang"]
        curr_map = Map.objects.get(map_name = "Flaring Phoenix")
        counter_score = calculate_counter_score(top_brawler, enemy_team, curr_map)
        self.assertGreaterEqual(counter_score, 0.0)
        self.assertLessEqual(counter_score, 1,0)



