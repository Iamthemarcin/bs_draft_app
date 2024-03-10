from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import F, FloatField

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Mode(models.Model):
    mode_name = models.CharField(max_length = 15, primary_key = True)
    mode_icon = models.CharField(max_length = 200)

    def __str__(self):
        return self.mode_name

class Map(models.Model):
    map_name = models.CharField(max_length = 30)
    mode_name = models.ForeignKey(Mode, on_delete = models.CASCADE)
    games_played = models.IntegerField()
    def __str__(self):
        return self.map_name

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

    def __str__(self):
        return self.brawler_name


class WinRateQuerySet(models.QuerySet):
    def calc_win_rate(self):
        return self.annotate(actual_win_rate=F('games_won')/F('games_played'))
    def calc_viability(self):
        ayaya = self.annotate(viability = (F('games_won')/F('games_played')) * F('use_rate'))
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
        return self.map_name.map_name + ' ' + self.brawler_name.brawler_name


    

    
class Player(models.Model):
    player_tag = models.CharField(max_length = 20, primary_key = True)

class LastPlayerChecked(models.Model):
    last_player_checked = models.IntegerField(primary_key= True, default = 0)
    class Meta:
        verbose_name_plural = "LastPlayerChecked"

# Create your models here.
