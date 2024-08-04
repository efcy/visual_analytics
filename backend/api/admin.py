from django.contrib import admin
from .models import Event, Game, Log, Image, FrameTime

# Register your models here.


admin.site.register(Event)
admin.site.register(Game)
admin.site.register(Log)
admin.site.register(Image)
admin.site.register(FrameTime)