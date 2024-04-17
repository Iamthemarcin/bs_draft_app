from django.contrib import admin
from .models import Mode, Map, Brawler, WinRate, Player, LastPlayerChecked, BrawlerClass


register_me = [Mode, Map, Brawler, WinRate, Player, LastPlayerChecked, BrawlerClass]
for me in register_me:
    admin.site.register(me)




# Register your models here.
