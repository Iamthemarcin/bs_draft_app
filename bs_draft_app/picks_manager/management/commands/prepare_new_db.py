from django.core.management.base import BaseCommand, CommandError
#created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB 


#this script updates the brawlers with an api call and then assigns them properties from ma excel sheet.
def prepare_new_db():
    Manager = ManageDB()
    Manager.update_brawler_classes()

    Manager.get_player_tags()
    print("Collected top players.")
    Manager.update_brawler_list()
    print("The brawler list has been prepared")
    Manager.update_brawler_pics()
    Manager.update_brawler_classes()
    print("Collecting map data")
    Manager.update_map_list_and_winrate(1000)
    print("Map data collection complete. Moving onto modes")
    Manager.update_modes()
    Manager.update_map_pics()
    
class Command(BaseCommand):
    help = 'Updates the database with new games from brawl API'
    def handle(self, *args, **options):
        prepare_new_db()
        self.stdout.write(self.style.SUCCESS('The new database has been prepared.'))
