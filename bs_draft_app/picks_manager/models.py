from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import F, ExpressionWrapper, FloatField
from decimal import Decimal
from rest_framework import serializers  # type: ignore
import datetime


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Mode(models.Model):
    mode_name = models.CharField(max_length = 15, primary_key = True)
    mode_icon = models.CharField(max_length = 200)
    mode_color = models.CharField(max_length = 30)
    def __str__(self):
        return self.mode_name

class Map(models.Model):
    map_name = models.CharField(max_length = 30)
    mode_name = models.ForeignKey(Mode, on_delete = models.CASCADE)
    games_played = models.IntegerField()
    image_url = models.CharField(max_length=100)
    def __str__(self):
        return self.map_name


class BrawlerClass(models.Model):

    class_name = models.CharField(max_length = 25, primary_key=True)
    countered_by = models.CharField(max_length = 100)

    def __str__(self):
        return self.class_name
    class Meta:
        verbose_name_plural = "Brawler classes"

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

    def __str__(self):
        return self.brawler_name


class WinRateQuerySet(models.QuerySet):
    def calc_win_rate(self):
        return self.annotate(win_rate=F('games_won')/F('games_played'))
    def calc_viability(self):
        ayaya = self.annotate(viability = ExpressionWrapper(F('games_won')*Decimal('1.75')/(F('games_played')) + F('use_rate'),output_field = FloatField())).filter(games_won__gt = 10) ##if less than 4 games i dont care bout u sorry mr object.
        return ayaya
class WinRate(models.Model):
    class Meta:
        unique_together = (('brawler_name', 'map_name'),)
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

class LastPlayerChecked(models.Model):
    last_player_checked = models.IntegerField(primary_key= True, default = 0)
    class Meta:
        verbose_name_plural = "LastPlayerChecked"
