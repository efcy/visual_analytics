from django.db import models
from common.models import Log

"""
    All Models for Motion Representations
"""

class MotionFrame(models.Model):
    log = models.ForeignKey(Log,on_delete=models.CASCADE, related_name='motionframe')
    frame_number = models.IntegerField(blank=True, null=True)
    frame_time = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Motion Frames"
        indexes = [
            models.Index(fields=['log', 'frame_number']),
        ]
        unique_together = ('log', 'frame_number')

class IMUData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='imudata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "IMU Data"


class FSRData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='fsrdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "FSR Data"


class ButtonData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='buttondata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Button Data"


class SensorJointData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='sensorjointdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Sensor Joint Data"


class AccelerometerData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='accelerometerdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Accelerometer Data"


class InertialSensorData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='inertialsensordata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Inertial Sensor Data"


class MotionStatus(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='motionstatus')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"
    
    class Meta:
        verbose_name_plural = "Motion Status"


class MotorJointData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='motorjointdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Motor Joint Data"


class GyrometerData(models.Model):
    frame = models.ForeignKey(MotionFrame,on_delete=models.CASCADE, related_name='gyrometerdata')
    representation_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.frame}--{self.__class__.__name__}"

    class Meta:
        verbose_name_plural = "Gyrometer Data"
