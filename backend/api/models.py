from django.db import models
#from django.contrib.gis.db import models as geo_models
from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    time = DateTimeRangeField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    # location = geo_models.PointField() # TODO figure out how to use this with our postgres and with testing 
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE, related_name='games')
    #related names attribute is to get all objects related to a 'parent' object. for example Event.games.all() returns all games for a specified event
    team1 = models.CharField(max_length=100,blank=True, null=True)
    team2 = models.CharField(max_length=100,blank=True, null=True)
    half = models.CharField(max_length=100,blank=True, null=True)
    is_testgame = models.BooleanField(blank=True, null=True)
    head_ref = models.CharField(max_length=100, blank=True, null=True)
    assistent_ref = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    # score

    class Meta:
        unique_together = ('event', 'start_time', 'half')

    def __str__(self):
        return f"{self.start_time}: {self.team1} vs {self.team2} {self.half}"

class RobotData(models.Model):
    # TODO check this foreignkey thing: the related_name stuff looks wrong
    game = models.ForeignKey(Game,on_delete=models.CASCADE,related_name='robot_data')
    robot_version = models.CharField(max_length=5, blank=True, null=True)
    player_number = models.IntegerField(blank=True, null=True)
    head_number = models.IntegerField(blank=True, null=True)
    body_serial = models.CharField(max_length=20, blank=True, null=True)
    head_serial = models.CharField(max_length=20, blank=True, null=True)
    representations = models.JSONField(blank=True, null=True)
    sensor_log_path = models.CharField(max_length=200, blank=True, null=True)
    log_path = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('game', 'player_number', 'head_number')

    def __str__(self):
        return f"{self.player_number} - {self.head_number}"

class SensorLog(models.Model):
    robotdata = models.ForeignKey(RobotData,on_delete=models.CASCADE, related_name='sensorlogs')
    sensor_frame_number = models.IntegerField(blank=True, null=True)
    sensor_frame_time = models.IntegerField(blank=True, null=True)
    representation_name = models.CharField(max_length=40, blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)
    
class Image(models.Model):
    class Camera(models.TextChoices):
        TOP = "TOP", _("Top")
        BOTTOM = "BOTTOM", _("Bottom")
    class Type(models.TextChoices):
        raw = "RAW", _("raw")
        jpeg = "JPEG", _("jpeg")
    # FIXME playernumber, robotnumber and serial must be part of the foreign key, we can change robots midgame when one robot breaks
    log = models.ForeignKey(RobotData,on_delete=models.CASCADE,related_name='images')
    camera = models.CharField(max_length=10, choices=Camera, blank=True, null=True)
    type = models.CharField(max_length=10, choices=Type, blank=True, null=True)
    frame_number = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('log', 'camera', 'type', 'frame_number')

class ImageAnnotation(models.Model):
    image= models.ForeignKey(Image,on_delete=models.CASCADE,related_name='ImageAnnotation')
    type  = models.CharField(max_length=100)


class FrameTime(models.Model):
    """dummy model to test timeline"""
    frame_number = models.IntegerField(blank=True, null=True)
    frame_time   = models.IntegerField(blank=True,null=True)