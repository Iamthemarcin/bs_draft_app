from django.core.management.base import BaseCommand, CommandError
# created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB
from picks_manager.models import ScannedData


def update_db(scan_ammount, debug = False):
    Manager = ManageDB()
    scanned_games = Manager.update_map_list_and_winrate(
        scan_ammount, debug=debug)
    print(f"scanned {scanned_games} ranked games")
    scan_data = ScannedData.objects.first()
    scan_data.scanned_games += scanned_games
    scan_data.save()


class Command(BaseCommand):
    help = 'Updates the database with new games from brawl API'

    def add_arguments(self, parser):
        parser.add_argument("scan_ammount", type=int)
        parser.add_argument('-dbg', '--debug',  action='store_true',  help='Debug location data fetch from google')

    def handle(self, *args, **options):
        scan_ammount = options["scan_ammount"]
        debug = False
        if options["debug"]:
            debug = True
        update_db(scan_ammount, debug = debug)
        self.stdout.write(self.style.SUCCESS(
            'You ran this instance of update_db as a command'))
