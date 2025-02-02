from django.core.management.base import BaseCommand, CommandError
#created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB




class Command(BaseCommand):
    help = 'Updates the database with new games from brawl API'
    def handle(self, *args, **options):
        ManageDB().update_brawlers_counterability()
        self.stdout.write(self.style.SUCCESS('The WinRates counterabiltiy scores have been updated.'))
