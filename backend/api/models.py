from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_day = models.DateField(blank=True, null=True)
    end_day = models.DateField(blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True) # latitude and longitude in Degrees, minutes, and seconds (DMS)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    #related names attribute is to get all objects related to a 'parent' object. 
    # for example Event.games.all() returns all games for a specified event
    event_id = models.ForeignKey(Event,on_delete=models.CASCADE, related_name='games')
    team1 = models.CharField(max_length=100,blank=True, null=True)
    team2 = models.CharField(max_length=100,blank=True, null=True)
    half = models.CharField(max_length=100,blank=True, null=True)
    is_testgame = models.BooleanField(blank=True, null=True)
    head_ref = models.CharField(max_length=100, blank=True, null=True)
    assistent_ref = models.CharField(max_length=100, blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    score = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    #class Meta:
    #    unique_together = ('event_id', 'start_time', 'half')

    def __str__(self):
        return f"{self.start_time}: {self.team1} vs {self.team2} {self.half}"

class Log(models.Model):
    game_id = models.ForeignKey(Game,on_delete=models.CASCADE,related_name='robot_data')
    robot_version = models.CharField(max_length=5, blank=True, null=True)
    player_number = models.IntegerField(blank=True, null=True)
    head_number = models.IntegerField(blank=True, null=True)
    body_serial = models.CharField(max_length=20, blank=True, null=True)
    head_serial = models.CharField(max_length=20, blank=True, null=True)
    representation_list = models.JSONField(blank=True, null=True)
    log_path = models.CharField(max_length=200, blank=True, null=True)
    combined_log_path = models.CharField(max_length=200, blank=True, null=True)
    sensor_log_path = models.CharField(max_length=200, blank=True, null=True)

    # TODO build a log_insert_status model which can hold those information, we would also need that
    # for all other representations that we might want to add to the database
    num_cognition_frames = models.IntegerField(blank=True, null=True)
    num_motion_frames = models.IntegerField(blank=True, null=True)
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
    log = models.ForeignKey(Log,on_delete=models.CASCADE,related_name='images')
    camera = models.CharField(max_length=10, choices=Camera, blank=True, null=True)
    type = models.CharField(max_length=10, choices=Type, blank=True, null=True)
    frame_number = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    blurredness_value = models.IntegerField(blank=True, null=True)
    brightness_value = models.IntegerField(blank=True, null=True)
    resolution =  models.CharField(max_length=20, blank=True, null=True)

    #class Meta:
    #    unique_together = ('log', 'camera', 'type', 'frame_number')

    def __str__(self):
        return f"{self.log}-{self.camera}-{self.type}-{self.frame_number}"


class Annotation(models.Model):
    image= models.ForeignKey(Image,on_delete=models.CASCADE,related_name='Annotation')
    annotation_id  = models.CharField(max_length=100)
    annotation = models.JSONField(blank=True, null=True)


class CognitionRepresentation(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='cognition_repr')
    frame_number = models.IntegerField(blank=True, null=True)
    representation_name = models.CharField(max_length=100)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.log_id}-{self.frame_number}-{self.representation_name}"


class MotionRepresentation(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='motion_repr')
    sensor_frame_number = models.IntegerField(blank=True, null=True)
    sensor_frame_time = models.IntegerField(blank=True, null=True)
    representation_name = models.CharField(max_length=40, blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.log_id}-{self.sensor_frame_number}-{self.representation_name}"


class BehaviorOption(models.Model):
    # we need to keep the reference to the log here because the xabsl code could change between logs,
    # changing the options and the states in it as well
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='behavior_options')
    # this id depends on the order it appears in the BehaviorStateComplete representation
    # we need this to get the actual option id during insertion of BehaviorStateSparse
    # lookup looks like this: client.list(log_id=log_id, xabsl_internal_id=<id in BehaviorStateSparse>)
    xabsl_internal_option_id = models.IntegerField(blank=True, null=True)
    option_name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{self.log_id}-{self.option_name}"

class BehaviorOptionState(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='behavior_options_states')
    option_id = models.ForeignKey(BehaviorOption, on_delete=models.CASCADE, related_name='behavior_options_states')
    # state id within an option - this is the id BehaviorFrameOption.activeState refers to
    xabsl_internal_state_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    target = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.log_id}-{self.name}"

    # CONSTRAINT behavior_options_states_constraint UNIQUE (log_id, options_id, id)


class BehaviorFrameOption(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='behavior_frame_option')
    options_id = models.ForeignKey(BehaviorOption,on_delete=models.CASCADE, related_name='behavior_frame_option')
    active_state = models.ForeignKey(BehaviorOptionState,on_delete=models.CASCADE, related_name='behavior_frame_option')

    # parent can't be a foreign key for now because we identify the root option with -1. 
    # TODO add root option with id -1 => would mean we manually need to create the id column and handle the primary key behavior
    #parent = models.ForeignKey(BehaviorOption,to_field='id', on_delete=models.CASCADE, related_name='behavior_frame_options_parent')
    parent = models.IntegerField(blank=True, null=True)
    frame = models.IntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    time_of_execution = models.IntegerField(blank=True, null=True)
    state_time = models.IntegerField(blank=True, null=True)


class XabslSymbol(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='xabsl_symbols')
    frame = models.IntegerField(blank=True, null=True)
    symbol_type = models.CharField(max_length=20, blank=True, null=True)
    symbol_name = models.CharField(max_length=100, blank=True, null=True)
    symbol_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['log_id', 'frame']),
        ]
        unique_together = ('log_id', 'frame', 'symbol_type', 'symbol_name')

class XabslSymbol2(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='xabsl_symbols2')
    frame = models.IntegerField(blank=True, null=True)
    output_decimal = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['log_id', 'frame']),
        ]
        unique_together = ('log_id', 'frame')