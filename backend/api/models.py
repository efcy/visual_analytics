from django.db import models
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_day = models.DateField(blank=True, null=True)
    end_day = models.DateField(blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True) # latitude and longitude in Degrees, minutes, and seconds (DMS)
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
    game = models.ForeignKey(Game,on_delete=models.CASCADE,related_name='robot_data')
    robot_version = models.CharField(max_length=5, blank=True, null=True)
    player_number = models.IntegerField(blank=True, null=True)
    head_number = models.IntegerField(blank=True, null=True)
    body_serial = models.CharField(max_length=20, blank=True, null=True)
    head_serial = models.CharField(max_length=20, blank=True, null=True)
    representation_list = models.JSONField(blank=True, null=True)
    sensor_log_path = models.CharField(max_length=200, blank=True, null=True)
    log_path = models.CharField(max_length=200, blank=True, null=True)

    num_jpg_bottom = models.IntegerField(blank=True, null=True)
    num_jpg_top = models.IntegerField(blank=True, null=True)
    num_bottom = models.IntegerField(blank=True, null=True)
    num_top = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.log_path}"

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

    def __str__(self):
        return f"{self.log}-{self.camera}-{self.type}-{self.frame_number}"


class Annotation(models.Model):
    image= models.ForeignKey(Image,on_delete=models.CASCADE,related_name='Annotation')
    annotation_id  = models.CharField(max_length=100)
    annotation = models.JSONField(blank=True, null=True)


class CognitionRepresentation(models.Model):
    log = models.ForeignKey(RobotData,on_delete=models.CASCADE, related_name='cognition_repr')
    frame_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ('log', 'frame_number', 'name')

    def __str__(self):
        return f"{self.log}-{self.frame_number}-{self.name}"


class MotionRepresentation(models.Model):
    robotdata = models.ForeignKey(RobotData,on_delete=models.CASCADE, related_name='motion_repr')
    sensor_frame_number = models.IntegerField(blank=True, null=True)
    sensor_frame_time = models.IntegerField(blank=True, null=True)
    representation_name = models.CharField(max_length=40, blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)