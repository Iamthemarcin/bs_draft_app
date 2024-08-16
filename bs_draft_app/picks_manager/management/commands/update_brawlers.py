from django.core.management.base import BaseCommand, CommandError
#created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB 


#this script updates the brawlers with an api call and then assigns them properties from ma excel sheet.
def update_brawlers():
    Manager = ManageDB()
    Manager.update_brawler_list()

class Command(BaseCommand):
    help = 'Updates the database with new games from brawl API'
    def handle(self, *args, **options):
        update_brawlers()
        self.stdout.write(self.style.SUCCESS('The brawlers have been updated.'))
