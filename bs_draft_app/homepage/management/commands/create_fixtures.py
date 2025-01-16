from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from picks_manager.models import Mode, Map, Brawler, WinRate, Player, ScannedData, BrawlerClass, HeadToHead, Synergy
import json
import os

class Command(BaseCommand):
    help = 'Creates fixture files with a limited number of rows'

    def handle(self, *args, **kwargs):
        models = [Mode, Map, Brawler, WinRate, Player, ScannedData, BrawlerClass, HeadToHead, Synergy]

        for model in models:
            model_name = model.__name__
            self.stdout.write(f"Dumping {model_name}...")

            # Limit rows, no need for all 200k

            data = serialize('json', model.objects.all()[:5000])

            fixture_filename = os.path.join('fixtures', f'{model_name.lower()}_fixture.json')
            with open(fixture_filename, 'w') as f:
                f.write(data)

            self.stdout.write(f"Fixture for {model_name} created: {fixture_filename}")
