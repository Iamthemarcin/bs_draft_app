from django.contrib import admin
from .models import Mode, Map, Brawler, WinRate, Player, ScannedData, BrawlerClass, HeadToHead


register_me = [Mode, Map, Brawler, Player, ScannedData, BrawlerClass]
for me in register_me:
    admin.site.register(me)

# Register your models here.
@admin.register(WinRate)
class WinRateAdmin(admin.ModelAdmin):
    list_display = ('brawler_name', 'map_name', 'use_rate', 'games_played', 'games_won')  
    list_filter = ('brawler_name', 'map_name') 
    ordering = ['brawler_name__brawler_name'] 

@admin.register(HeadToHead)
class WinRateAdmin(admin.ModelAdmin):
    list_display = ('brawler_a', 'brawler_b', 'map', 'matches_played', 'win_rate_a')  
    list_filter = ('brawler_a', 'brawler_b') 
    ordering = ['brawler_a__brawler_name'] 
