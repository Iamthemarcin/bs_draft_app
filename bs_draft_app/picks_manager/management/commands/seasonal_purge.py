from django.core.management.base import BaseCommand, CommandError
#created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB 
from picks_manager.models import WinRate, Map


def seasonal_purge():
    WinRate.objects.all().delete()
    Map.objects.all().delete()
    
class Command(BaseCommand):
    help = 'Updates the database with new games from brawl API'
    def handle(self, *args, **options):
        seasonal_purge()
        self.stdout.write(self.style.SUCCESS('You have purged all the Win Rate and maps records from this season.'))

