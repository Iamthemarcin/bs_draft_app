import os
from django.contrib import admin
from .models import Mode, Map, Brawler, WinRate, Player, ScannedData, BrawlerClass, HeadToHead, Synergy


# I only want silk on dev environment
if os.getenv('DEBUGPY_DJANGO'):
    from silk.models import Profile, SQLQuery, Request
    register_me = [Profile, SQLQuery, Request]
    for me in register_me:
        admin.site.register(me)



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
class HeadToHeadAdmin(admin.ModelAdmin):
    list_display = ('brawler_a', 'brawler_b', 'map', 'matches_played', 'win_rate_a')
    list_filter = ('brawler_a', 'brawler_b')
    ordering = ['brawler_a__brawler_name']

@admin.register(Synergy)
class SynergyAdmin(admin.ModelAdmin):
    list_display = ('brawler_a', 'brawler_b', 'map', 'matches_played', 'win_rate_together')
    list_filter = ('brawler_a', 'brawler_b')
    ordering = ['brawler_a__brawler_name']
