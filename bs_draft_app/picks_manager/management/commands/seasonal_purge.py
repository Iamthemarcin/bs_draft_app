from django.core.management.base import BaseCommand, CommandError
#created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB 
from picks_manager.models import WinRate, Map, ScannedData


def seasonal_purge():
    WinRate.objects.all().delete()
    Map.objects.all().delete()
    ScannedData.all().delete()

    
class Command(BaseCommand):
    help = 'Purges the database of all the game records from current season.'
    def handle(self, *args, **options):
        seasonal_purge()
        self.stdout.write(self.style.SUCCESS('You have purged all the Win Rate and maps records from this season.'))

