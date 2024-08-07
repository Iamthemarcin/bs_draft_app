from django.core.management.base import BaseCommand, CommandError
#created this as a command to fix use rate on prod
from picks_manager.views import CleaningDB 


def fix_ur():
    C = CleaningDB()
    C.fix_use_rate()
    
class Command(BaseCommand):
    help = 'Fixes the use rate whenever it gets bugged. A workaround.'
    def handle(self, *args, **options):
        fix_ur()
        self.stdout.write(self.style.SUCCESS('You have (probably) fixed the use rate'))

