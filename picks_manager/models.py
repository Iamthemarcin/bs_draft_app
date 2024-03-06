from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

class WinRate(models.Model):
    class Meta:
        unique_together = (('brawler_name', 'map_name'),)
    id = models.AutoField(primary_key=True)
    brawler_name = models.ForeignKey(Brawler, on_delete = models.CASCADE)
    map_name = models.ForeignKey(Map, on_delete = models.CASCADE)
    use_rate = models.FloatField(validators=PERCENTAGE_VALIDATOR)
    games_played = models.IntegerField()
    games_won = models.IntegerField()
    def _get_win_rate(self):
        return self.games_won/self.games_played
    win_rate = property(_get_win_rate)
    
    def __str__(self):
        return self.map_name.map_name + ' ' + self.brawler_name.brawler_name
    
class Player(models.Model):
    player_tag = models.CharField(max_length = 20, primary_key = True)

class LastPlayerChecked(models.Model):
    last_player_checked = models.IntegerField(primary_key= True, default = 0)
    class Meta:
        verbose_name_plural = "LastPlayerChecked"

# Create your models here.
