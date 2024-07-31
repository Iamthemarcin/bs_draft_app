from django.core.management.base import BaseCommand, CommandError
#created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB 

def update_db():
    scan_ammount = 15
    Manager = ManageDB()
    scanned_games = Manager.update_map_list_and_winrate(scan_ammount)
    print(f"scanned {scanned_games} ranked games")
    
class Command(BaseCommand):
    help = 'Updates the database with new games from brawl API'
    def handle(self, *args, **options):
        update_db()
        self.stdout.write(self.style.SUCCESS('You ran this instance of update_db as a command'))

