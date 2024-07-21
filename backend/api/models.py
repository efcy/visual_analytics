from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        # TODO is this function just for the admin panel?
        return self.name


class Game(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='games')
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)


class Log(models.Model):
    player_number = models.IntegerField()
    game = models.ForeignKey(Game,on_delete=models.CASCADE,related_name='logs')
