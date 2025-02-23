from django.contrib import admin
from .models import (
    MotionFrame,
    IMUData,
    FSRData,
    ButtonData,
    SensorJointData,
    AccelerometerData,
    InertialSensorData,
    MotionStatus,
    MotorJointData,
    GyrometerData,
)


admin.site.register(MotionFrame)

admin.site.register(IMUData)
admin.site.register(FSRData)
admin.site.register(ButtonData)
admin.site.register(SensorJointData)
admin.site.register(AccelerometerData)
admin.site.register(InertialSensorData)
admin.site.register(MotionStatus)
admin.site.register(MotorJointData)
admin.site.register(GyrometerData)
