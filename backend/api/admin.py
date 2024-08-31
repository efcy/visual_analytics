from django.contrib import admin
from .models import Event, Game, RobotData, Image, SensorLog, Annotation


class ImageAdmin(admin.ModelAdmin):
    search_fields = ['log__log_path','image_url__icontains']
    list_display = ["log","frame_number"]

class RobotDataAdmin(admin.ModelAdmin):
    search_fields = ['log_path__icontains']

# Register your models here.
admin.site.register(Event)
admin.site.register(Game)
admin.site.register(RobotData, RobotDataAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(SensorLog)
admin.site.register(Annotation)
