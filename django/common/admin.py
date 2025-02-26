from django.contrib import admin
from .models import Event, Game, Log, LogStatus, Experiment
from unfold.admin import ModelAdmin

class GameAdmin(ModelAdmin):
    list_display = ("event_id", "get_id", "team1", "team2", "half", "is_testgame")

    def get_id(self, obj):
        return obj.id

    get_id.short_description = "Game ID"


class LogAdmin(ModelAdmin):
    search_fields = [
        "game_id__team1__icontains",
        "game_id__team2__icontains",
        "head_number",
        "player_number",
    ]
    list_display = [
        "get_game_id",
        "get_id",
        "get_team1",
        "get_team2",
        "get_half",
        "player_number",
        "head_number",
        "get_start_time",
        "is_test",
    ]

    def get_game_id(self, obj):
        return obj.game.id

    def get_id(self, obj):
        return obj.id

    def get_team1(self, obj):
        return obj.game.team1

    def get_team2(self, obj):
        return obj.game.team2

    def get_half(self, obj):
        return obj.game.half

    def get_start_time(self, obj):
        return obj.game.start_time

    def is_test(self, obj):
        return obj.game.is_testgame

    get_id.short_description = "Log ID"
    get_game_id.short_description = "Game ID"
    get_start_time.short_description = "Time"
    get_team1.short_description = "Team 1"
    get_team2.short_description = "Team 2"


class LogStatusAdmin(ModelAdmin):
    list_display = ["get_log_id"]

    def get_log_id(self, obj):
        return obj.log.id

    get_log_id.short_description = "Log ID"

@admin.register(Event)
@admin.register(Experiment)
class CustomAdminClass(ModelAdmin):
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(LogStatus, LogStatusAdmin)
