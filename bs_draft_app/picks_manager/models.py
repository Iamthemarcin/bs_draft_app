from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.management import call_command
from django.db.models import F, ExpressionWrapper, FloatField
from decimal import Decimal
from rest_framework import serializers  # type: ignore
import datetime
from django.contrib import admin



PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Mode(models.Model):
    mode_name = models.CharField(max_length = 15, primary_key = True)
    mode_icon = models.CharField(max_length = 200)
    mode_color = models.CharField(max_length = 30)
    def __str__(self):
        return self.mode_name
    class Meta:
        app_label = 'picks_manager'

class Map(models.Model):
    map_name = models.CharField(max_length = 30)
    mode_name = models.ForeignKey(Mode, on_delete = models.CASCADE)
    games_played = models.IntegerField()
    image_url = models.CharField(max_length=100)


    def __str__(self):
        return self.map_name

    class Meta:
        ordering = ("games_played",)

class BrawlerClass(models.Model):

    class_name = models.CharField(max_length = 25, primary_key=True)
    countered_by = models.CharField(max_length = 100)

    def __str__(self):
        return self.class_name
    class Meta:
        verbose_name_plural = "Brawler classes"

class BrawlerManager(models.Manager):
    def get_or_update(self, brawler_name):
        try:
            return self.get(brawler_name__iexact=brawler_name)
        except Brawler.DoesNotExist:
            print(f"{brawler_name} isn't in the database. Updating database with update_brawlers command.")
            try:
                call_command('update_brawlers')  # Executes update_brawlers.py management command
            except Exception as e:
                print(f"Failed to run update_brawlers command: {e}")
                return None
            # Try fetching the brawler again after the update
            try:
                return Brawler.objects.get(brawler_name__iexact=brawler_name)
            except Brawler.DoesNotExist:
                print(f"{brawler_name} still not found after update.")
                return None


class Brawler(models.Model):

    LEG = "LEGENDARY"
    MYTH = "MYTHICAL"
    EPIC = "EPIC"
    SR = "SUPER RARE"
    RARE = "RARE"

    BRAWLER_RARITIES = [
        (LEG, "Legendary"),
        (MYTH, "Mythical"),
        (EPIC,  "Epic"),
        (SR, "Super rare"),
        (RARE, "Rare"),
    ]
    brawler_name = models.CharField(primary_key=True, max_length = 20)
    rarity = models.CharField(max_length = 11, choices = BRAWLER_RARITIES, default = RARE)
    image_url = models.CharField(max_length = 200)
    brawler_class = models.ForeignKey(BrawlerClass, max_length = 25, on_delete = models.DO_NOTHING)
    easy_to_counter = models.CharField(max_length=6, default = "no")
    has_pets = models.CharField(max_length=6, default = "no")
    countered_by_pets = models.CharField(max_length=6, default = "no")
    counters_pets = models.CharField(max_length=6, default = "no")
    hz_sitter = models.CharField(max_length=6, default="no")
    gem_carrier = models.CharField(max_length=6, default="no")
    objects = BrawlerManager()

    def __str__(self):
        return self.brawler_name





class WinRateQuerySet(models.QuerySet):
    def calc_win_rate(self):
        return self.annotate(win_rate=F('games_won')/F('games_played'))
    def calc_viability(self):
        ayaya = self.annotate(viability = ExpressionWrapper(F('games_won')*Decimal('1.75')/(F('games_played')) + F('use_rate'),output_field = FloatField())).filter(games_won__gt = 10) ##if less than 10 games i dont care bout u sorry mr object.
        return ayaya


class WinRate(models.Model):
    class Meta:
        unique_together = (('brawler_name', 'map_name'),)
        ordering = ['brawler_name__brawler_name']

    id = models.AutoField(primary_key=True)
    brawler_name = models.ForeignKey(Brawler, on_delete = models.CASCADE)
    map_name = models.ForeignKey(Map, on_delete = models.CASCADE)
    use_rate = models.FloatField(validators=PERCENTAGE_VALIDATOR)
    games_played = models.IntegerField()
    games_won = models.IntegerField()
    objects = WinRateQuerySet.as_manager()
    def __str__(self):
        return self.map_name.map_name + ', ' + self.brawler_name.brawler_name

class WinRateSerializer(serializers.Serializer):
    brawler_name = serializers.CharField(max_length = 30)
    use_rate = serializers.FloatField()
    win_rate = serializers.FloatField()
    viability = serializers.FloatField()

class Player(models.Model):
    player_tag = models.CharField(max_length = 20, primary_key = True)
    last_checked = models.DateField(default = datetime.date.today)

class ScannedData(models.Model):
    last_player_checked = models.IntegerField(primary_key= True, default = 0)
    scanned_games = models.IntegerField(default = 0)
    ammount_of_maps = models.IntegerField(default = 18)
    class Meta:
        verbose_name_plural = "ScannedData"

class HeadToHead(models.Model):

    brawler_a = models.ForeignKey(Brawler, on_delete= models.CASCADE, related_name="head_to_head_a")
    brawler_b = models.ForeignKey(Brawler, on_delete= models.CASCADE, related_name="head_to_head_b")

    map_name = models.ForeignKey(Map, on_delete= models.CASCADE)
    matches_played = models.PositiveIntegerField(default=0)
    matches_won_by_a = models.PositiveIntegerField(default=0)
    win_rate_a = models.FloatField(default=0.0)


    class Meta:
        unique_together = ('brawler_a', 'brawler_b', 'map_name')

    def save(self, *args, **kwargs):
        ##if i already have colt vs shelly in database, i dont want to save shelly vs colt in a different field
        if self.brawler_a.brawler_name > self.brawler_b.brawler_name:
            self.brawler_a, self.brawler_b = self.brawler_b, self.brawler_a

        if self.matches_played > 0:
            self.win_rate_a = self.matches_won_by_a / self.matches_played
        else:
            self.win_rate_a = 0.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brawler_a} vs {self.brawler_b} (Map: {self.map_name}, Mode: {self.map_name.mode_name})"

class Synergy(models.Model):
    brawler_a = models.ForeignKey(Brawler, on_delete= models.CASCADE, related_name="synergy_a")
    brawler_b = models.ForeignKey(Brawler, on_delete= models.CASCADE, related_name="synergy_b")

    map = models.ForeignKey(Map, on_delete= models.CASCADE)
    matches_played = models.PositiveIntegerField(default=0)
    matches_won = models.PositiveIntegerField(default=0)
    win_rate_together = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('brawler_a', 'brawler_b', 'map')
        verbose_name_plural = "Synergies"

    def save(self, *args, **kwargs):
        ##same as in headtoheads
        if self.brawler_a.brawler_name > self.brawler_b.brawler_name:
            self.brawler_a, self.brawler_b = self.brawler_b, self.brawler_a

        if self.matches_played > 0:
            self.win_rate_together = self.matches_won / self.matches_played
        else:
            self.win_rate_together = 0.0
        super().save(*args, **kwargs)
