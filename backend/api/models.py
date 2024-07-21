from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        # TODO is this function just for the admin panel?
        return self.name

class Game(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='games')
    #related names attribute is to get all objects related to a 'parent' object. for example Event.games.all() returns all games for a specified event
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)

class Log(models.Model):
    game = models.ForeignKey(Game,on_delete=models.CASCADE,related_name='logs')
    player_number = models.IntegerField()

class CameraMatrix(models.Model):
    log = models.ForeignKey(Log,on_delete=models.CASCADE,related_name='camera_matrix')
    frame_number = models.BigIntegerField()
    
class Image(models.Model):
    log = models.ForeignKey(Log,on_delete=models.CASCADE,related_name='images')
    type = models.CharField(max_length=100)

class ImageAnnotation(models.Model):
    image= models.ForeignKey(Image,on_delete=models.CASCADE,related_name='ImageAnnotation')
    type  = models.CharField(max_length=100)
