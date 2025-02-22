from django.contrib import admin
from .models import Event, Game, Log, LogStatus, Experiment


class GameAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'get_id', 'team1', 'team2', 'half', 'is_testgame')

    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'Game ID'


class LogAdmin(admin.ModelAdmin):
    search_fields = ['game_id__team1__icontains', 'game_id__team2__icontains', "head_number","player_number"]
    list_display = ["get_game_id", "get_id", "get_start_time", "get_team1", "get_team2", "player_number", "head_number", "is_test"]

    def get_game_id(self, obj):
        return obj.game_id.id

    def get_id(self, obj):
        return obj.id
    
    def get_start_time(self, obj):
        return obj.game_id.start_time
    
    def get_team1(self, obj):
        return obj.game_id.team1
    
    def get_team2(self, obj):
        return obj.game_id.team2

    def is_test(self, obj):
        return obj.game_id.is_testgame
    
    get_id.short_description = 'Log ID'
    get_game_id.short_description = 'Game ID'
    get_start_time.short_description = 'Time'
    get_team1.short_description = 'Team 1'
    get_team2.short_description = 'Team 2'


class LogStatusAdmin(admin.ModelAdmin):
    list_display = ["get_log_id"]

    def get_log_id(self, obj):
        return obj.log_id.id
    
    get_log_id.short_description = 'Log ID'


admin.site.register(Event)
admin.site.register(Game, GameAdmin)
admin.site.register(Experiment)
admin.site.register(Log)
admin.site.register(LogStatus, LogStatusAdmin)
