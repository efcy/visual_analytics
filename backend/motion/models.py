from django.db import models
from api.models import Log

"""
    All Models for Motion Representations
"""

class MotionFrame(models.Model):
    log_id = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='motionframe')
    frame_number = models.IntegerField(blank=True, null=True)
    frame_time = models.IntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['log_id', 'frame_number']),
        ]
        unique_together = ('log_id', 'frame_number')

class IMUData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='imudata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"


class FSRData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='fsrdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"


class ButtonData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='buttondata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"


class SensorJointData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='sensorjointdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"


class AccelerometerData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='accelerometerdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"


class InertialSensorData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='inertialsensordata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"


class MotionStatus(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='motionstatus')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"


class MotorJointData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='motorjointdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"


class GyrometerData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='gyrometerdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
