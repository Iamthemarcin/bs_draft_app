from django.test import TransactionTestCase
from picks_manager.models import Map
from homepage.views import get_top_brawlers, get_top_brawlers_regression
class MainDatabaseTest(TransactionTestCase):
    """These tests require lots of data to be of any use, make sure the functions don't alter the data in any way."""

    databases = {'default'}  # Use the 'default' (main) database

    def test_get_top_brawlers_regression(self):
        my_map = list(Map.objects.all())
        print('u set uyp asdhrftdsuef', my_map)
        get_top_brawlers_regression(my_map, 48)
