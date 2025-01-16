from django.test import TestCase
from picks_manager.models import Map
from homepage.views import get_top_brawlers, get_top_brawlers_regression
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
