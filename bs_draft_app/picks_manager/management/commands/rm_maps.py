from django.core.management.base import BaseCommand, CommandError
#created this as a command to debug my cronjob easier
from picks_manager.views import ManageDB 
from picks_manager.models import Map


def rm_maps(removal_amm):

    names = Map.objects.all().order_by('games_played').values_list('map_name')[:removal_amm]
    Map.objects.filter(map_name__in = names).delete()
    print('hi')
class Command(BaseCommand):
    help = 'Updates the database with new games from brawl API'
    def handle(self, *args, **options):
        removal_amm = options['removal_amm']

        rm_maps(removal_amm)
        self.stdout.write(self.style.SUCCESS(f'You removed {removal_amm} least played maps'))

    def add_arguments(self, parser):
        parser.add_argument('removal_amm', type=int)
