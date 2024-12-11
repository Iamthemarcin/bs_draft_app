from django.core.management.base import BaseCommand, CommandError
# created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB
from picks_manager.models import ScannedData

try:
    from silk.profiling.profiler import silk_profile
except:
    pass

@silk_profile(name="Updating the Database")
def update_db(scan_ammount):
    Manager = ManageDB()
    scanned_games = Manager.update_map_list_and_winrate(
        scan_ammount, debug=True)
    print(f"scanned {scanned_games} ranked games")
    scan_data = ScannedData.objects.first()
    scan_data.scanned_games += scanned_games
    scan_data.save()


class Command(BaseCommand):
    help = 'Updates the database with new games from brawl API'

    def add_arguments(self, parser):
        parser.add_argument("scan_ammount", type=int)

    @silk_profile(name="Update Database")
    def handle(self, *args, **options):
        scan_ammount = options["scan_ammount"]
        update_db(scan_ammount)
        self.stdout.write(self.style.SUCCESS(
            'You ran this instance of update_db as a command'))
