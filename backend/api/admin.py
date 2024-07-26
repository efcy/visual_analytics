from django.contrib import admin
from .models import Event, Game, Log

# Register your models here.


admin.site.register(Event)
admin.site.register(Game)
admin.site.register(Log)