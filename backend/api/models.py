from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.conf import settings


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

    class Meta:
        unique_together = ('event_id', 'start_time', 'half')

    def __str__(self):
        return f"{self.start_time}: {self.team1} vs {self.team2} {self.half}"


class VideoRecording(models.Model):
    # we model urls as json field because we can have multiple recordings and sometimes recordings are split up
    # also sometimes we do have a combined youtube video
    game_id = models.ForeignKey(Event,on_delete=models.CASCADE, related_name='recordings')
    urls = models.JSONField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    # TODO add calculated camera matrix here


class Experiment(models.Model):
    event_id = models.ForeignKey(Event,on_delete=models.CASCADE, related_name='experiments')
    # either the folder name if its an experiment of multiple robots or the logfile name
    name = models.CharField(max_length=100,blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('event_id', 'name')


class Log(models.Model):
    log_game = models.ForeignKey(Game, null=True, blank=True,
                                    on_delete=models.CASCADE)
    log_experiment = models.ForeignKey(Experiment, null=True, blank=True,
                                     on_delete=models.CASCADE)

    robot_version = models.CharField(max_length=5, blank=True, null=True)
    player_number = models.IntegerField(blank=True, null=True)
    head_number = models.IntegerField(blank=True, null=True)
    body_serial = models.CharField(max_length=20, blank=True, null=True)
    head_serial = models.CharField(max_length=20, blank=True, null=True)
    representation_list = models.JSONField(blank=True, null=True)
    log_path = models.CharField(max_length=200, blank=True, null=True)
    combined_log_path = models.CharField(max_length=200, blank=True, null=True)
    sensor_log_path = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.log_path}"
    
    @property
    def log_type(self):
        if self.log_game_id is not None:
            return self.log_game
        if self.log_experiment_id is not None:
            return self.log_experiment
        raise AssertionError("Neither 'log_game_id' nor 'log_experiment_id' is set")


class LogStatus(models.Model):
    log_id = models.OneToOneField(Log,on_delete=models.CASCADE,related_name='log_status', primary_key=True)
    # holds the number of frames that should be in the db for each representation
    FrameInfo = models.IntegerField(blank=True, null=True)
    BallModel = models.IntegerField(blank=True, null=True)
    BallCandidates = models.IntegerField(blank=True, null=True)
    BallCandidatesTop = models.IntegerField(blank=True, null=True)
    CameraMatrix = models.IntegerField(blank=True, null=True)
    CameraMatrixTop = models.IntegerField(blank=True, null=True)
    FieldPercept = models.IntegerField(blank=True, null=True)
    FieldPerceptTop = models.IntegerField(blank=True, null=True)
    GoalPercept = models.IntegerField(blank=True, null=True)
    GoalPerceptTop = models.IntegerField(blank=True, null=True)
    MultiBallPercept = models.IntegerField(blank=True, null=True)
    RansacLinePercept = models.IntegerField(blank=True, null=True)
    RansacCirclePercept2018 = models.IntegerField(blank=True, null=True)
    ShortLinePercept = models.IntegerField(blank=True, null=True)
    ScanLineEdgelPercept = models.IntegerField(blank=True, null=True)
    ScanLineEdgelPerceptTop = models.IntegerField(blank=True, null=True)
    OdometryData = models.IntegerField(blank=True, null=True)

    IMUData = models.IntegerField(blank=True, null=True)
    FSRData = models.IntegerField(blank=True, null=True)
    ButtonData = models.IntegerField(blank=True, null=True)
    SensorJointData = models.IntegerField(blank=True, null=True)
    AccelerometerData = models.IntegerField(blank=True, null=True)
    InertialSensorData = models.IntegerField(blank=True, null=True)
    MotionStatus = models.IntegerField(blank=True, null=True)
    MotorJointData = models.IntegerField(blank=True, null=True)
    GyrometerData = models.IntegerField(blank=True, null=True)

    num_cognition_frames = models.IntegerField(blank=True, null=True)
    num_motion_frames = models.IntegerField(blank=True, null=True)
    num_jpg_bottom = models.IntegerField(blank=True, null=True)
    num_jpg_top = models.IntegerField(blank=True, null=True)
    num_bottom = models.IntegerField(blank=True, null=True)
    num_top = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Log status"


class CognitionFrame(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='cognitionframe')
    frame_number = models.IntegerField(blank=True, null=True)


class MotionFrame(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='motionframe')
    frame_number = models.IntegerField(blank=True, null=True)


class Image(models.Model):
    class Camera(models.TextChoices):
        TOP = "TOP", _("Top")
        BOTTOM = "BOTTOM", _("Bottom")
    class Type(models.TextChoices):
        raw = "RAW", _("raw")
        jpeg = "JPEG", _("jpeg")
    # FIXME playernumber, robotnumber and serial must be part of the foreign key, we can change robots midgame when one robot breaks
    # FIXME it should be log_id instead of log to have consistency
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE,related_name='images')
    camera = models.CharField(max_length=10, choices=Camera, blank=True, null=True)
    type = models.CharField(max_length=10, choices=Type, blank=True, null=True)
    frame_number = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    blurredness_value = models.IntegerField(blank=True, null=True)
    brightness_value = models.IntegerField(blank=True, null=True)
    resolution =  models.CharField(max_length=11, blank=True, null=True) # 1640x1480x2

    class Meta:
        unique_together = ('log_id', 'camera', 'type', 'frame_number')

    def __str__(self):
        return f"{self.log_id}-{self.camera}-{self.type}-{self.frame_number}"


class Annotation(models.Model):
    image= models.OneToOneField(Image,on_delete=models.CASCADE,related_name='Annotation', primary_key=True)
    annotation = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class CognitionRepresentation(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='cognition_repr')
    frame_number = models.IntegerField(blank=True, null=True)
    # TODO maybe add frametime here
    representation_name = models.CharField(max_length=40)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.log_id}-{self.frame_number}-{self.representation_name}"
    
    class Meta:
        indexes = [
            models.Index(fields=['log_id', 'frame_number']),
        ]
        unique_together = ('log_id', 'frame_number', 'representation_name')


class MotionRepresentation(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='motion_repr')
    sensor_frame_number = models.IntegerField(blank=True, null=True)
    sensor_frame_time = models.IntegerField(blank=True, null=True)
    representation_name = models.CharField(max_length=40, blank=True, null=True)
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.log_id}-{self.sensor_frame_number}-{self.representation_name}"
    
    class Meta:
        indexes = [
            models.Index(fields=['log_id', 'sensor_frame_number']),
        ]
        unique_together = ('log_id', 'sensor_frame_number', 'representation_name')


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


class BehaviorFrameOption(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='behavior_frame_option')
    options_id = models.ForeignKey(BehaviorOption,on_delete=models.CASCADE, related_name='behavior_frame_option')
    active_state = models.ForeignKey(BehaviorOptionState,on_delete=models.CASCADE, related_name='behavior_frame_option')

    # parent can't be a foreign key for now because we identify the root option with -1. 
    # TODO add root option with id -1 => would mean we manually need to create the id column and handle the primary key behavior
    #parent = models.ForeignKey(BehaviorOption,to_field='id', on_delete=models.CASCADE, related_name='behavior_frame_options_parent')
    #parent = models.IntegerField(blank=True, null=True)
    frame = models.IntegerField(blank=True, null=True)
    #time = models.IntegerField(blank=True, null=True)
    #time_of_execution = models.IntegerField(blank=True, null=True)
    #state_time = models.IntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['log_id', 'frame', 'options_id']),
        ]
        unique_together = ('log_id', 'options_id', 'frame', 'active_state')


class XabslSymbolComplete(models.Model):
    log_id = models.OneToOneField(Log,on_delete=models.CASCADE, related_name='xabsl_symbol_complete', primary_key=True)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['log_id']),
        ]
        verbose_name_plural = "XabslSymbolComplete"

class XabslSymbolSparse(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='xabsl_symbol_sparse')
    frame = models.IntegerField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['log_id', 'frame']),
        ]
        unique_together = ('log_id', 'frame')
        verbose_name_plural = "XabslSymbolSparse"


class FrameFilter(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='frame_filter')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='frame_filter')
    frames = models.JSONField(blank=True, null=True)
    
    unique_together = ('log_id', 'user')
