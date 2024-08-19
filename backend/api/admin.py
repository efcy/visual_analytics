from django.contrib import admin
from .models import Event, Game, RobotData, Image, SensorLog


class ImageAdmin(admin.ModelAdmin):
    search_fields = ['image_url__icontains']

# Register your models here.
admin.site.register(Event)
admin.site.register(Game)
admin.site.register(RobotData)
admin.site.register(Image, ImageAdmin)
admin.site.register(SensorLog)
