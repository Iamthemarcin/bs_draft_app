from django.core.management.base import BaseCommand, CommandError
#created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB 


class Command(BaseCommand):
    help = 'Purges the database of all the game records from current season.'
    def handle(self, *args, **options):
        m = ManageDB()
        m.update_map_pics()
        self.stdout.write(self.style.SUCCESS('You have added thumbnail images to every map.'))

