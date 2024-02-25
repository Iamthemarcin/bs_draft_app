from django.contrib import admin
from .models import Mode, Map, Brawler, WinRate


register_me = [Mode, Map, Brawler, WinRate]
for me in register_me:
    admin.site.register(me)




# Register your models here.
