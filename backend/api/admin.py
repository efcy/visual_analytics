from django.contrib import admin
from .models import Event, Game, RobotData, Image, SensorLog

# Register your models here.
admin.site.register(Event)
admin.site.register(Game)
admin.site.register(RobotData)
admin.site.register(Image)
admin.site.register(SensorLog)
