from django.core.management.base import BaseCommand, CommandError
#created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB 
from picks_manager.models import WinRate, Map, ScannedData


def seasonal_purge():
    ammount_of_maps = input("How many maps are there in new season? ") 
    while True:
        try: 
            int(ammount_of_maps) 
            break
        except: ammount_of_maps = input("Please specify a number, ususally 18 or 24.")
    
    WinRate.objects.all().delete()
    Map.objects.all().delete()
    ScannedData.objects.all().delete()
    new_season_data = ScannedData(last_player_checked = 0, scanned_games = 0, ammount_of_maps = ammount_of_maps)
    new_season_data.save()
    
class Command(BaseCommand):
    help = 'Purges the database of all the game records from current season.'
    def handle(self, *args, **options):
        seasonal_purge()
        self.stdout.write(self.style.SUCCESS('You have purged all the Win Rate and maps records from this season.'))

