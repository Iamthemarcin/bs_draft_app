from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Mode(models.Model):
    mode_name = models.CharField(max_length = 15, primary_key = True)
    mode_icon = models.CharField(max_length = 200)

class Map(models.Model):
    map_name = models.CharField(max_length = 30)
    mode_name = models.ForeignKey(Mode, on_delete = models.CASCADE)

class Brawler(models.Model):

    LEG = "LEGENDARY"
    MYTH = "MYTHICAL"
    EPIC = "EPIC"
    SR = "SUPER RARE"
    RARE = "RARE"

    BRAWLER_RARITIES = [
        (LEG, "Legendaru"),
        (MYTH, "Mythical"),
        (EPIC,  "Epic"),
        (SR, "Super rare"),
        (RARE, "Rare"),
    ]
    brawler_name = models.CharField(primary_key=True, max_length = 20)
    rarity = models.CharField(max_length = 11, choices = BRAWLER_RARITIES, default = RARE)
    image_url = models.CharField(max_length = 200)

class WinRate(models.Model):
    class Meta:
        unique_together = (('brawler_name', 'map_name'),)

    brawler_name = models.ForeignKey(Brawler, on_delete = models.CASCADE,  primary_key=True)
    map_name = models.ForeignKey(Map, on_delete = models.CASCADE)
    win_rate = models.FloatField(validators=PERCENTAGE_VALIDATOR)
    use_rate = models.FloatField(validators=PERCENTAGE_VALIDATOR)

# Create your models here.
