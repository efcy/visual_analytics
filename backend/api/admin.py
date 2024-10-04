from django.contrib import admin
from django import forms
from .models import Event, Game, Log, Image, MotionRepresentation, CognitionRepresentation, Annotation, \
BehaviorOption, BehaviorOptionState, BehaviorFrameOption, XabslSymbol

class AnnotationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.none()

    class Meta:
        model = Annotation
        fields = '__all__'

    def clean_image(self):
        image_id = self.cleaned_data.get('image')
        if image_id:
            return Image.objects.get(id=image_id)
        return None

class ImageAdmin(admin.ModelAdmin):
    search_fields = ['log__log_path','image_url__icontains']
    list_display = ["log","frame_number"]


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

class AnnotationAdmin(admin.ModelAdmin):
    raw_id_fields = ('image',)
    list_per_page = 50

class CognitionRepresentationAdmin(admin.ModelAdmin):
    search_fields = ['frame_number__icontains', 'representation_name__icontains']
    list_display = ["log_id","frame_number", 'representation_name']
    list_per_page = 3000


class BehaviorOptionAdmin(admin.ModelAdmin):
    list_display = ('get_log_id', 'id', 'xabsl_internal_option_id', 'option_name')

    def get_log_id(self, obj):
        return obj.log_id.id
    get_log_id.short_description = 'Log ID'


class BehaviorOptionStateAdmin(admin.ModelAdmin):
    list_display = ('get_log_id', 'get_option_id','get_option_name','id', 'xabsl_internal_state_id', 'get_name')
    search_fields = ['option_id__option_name']
    def get_log_id(self, obj):
        return obj.log_id.id
    
    def get_option_id(self,obj):
        return obj.option_id.id
    
    def get_option_name(self,obj):
        return obj.option_id.option_name
    
    def get_name(self,obj):
        return obj.name

    get_log_id.short_description = 'Log ID'
    get_option_id.short_description = 'Option ID'
    get_option_name.short_description = 'Option Name'
    get_name.short_description = 'State Name'

class BehaviorFrameOptionAdmin(admin.ModelAdmin):
    list_display = ('get_log_id', 'get_option_id','get_option_name', 'get_active_state', 'frame')
    search_fields = ['options_id__option_name']
    def get_log_id(self, obj):
        return obj.log_id.id
    
    def get_option_id(self,obj):
        return obj.options_id.id
    
    def get_option_name(self,obj):
        return obj.options_id.option_name
    
    def get_active_state(self,obj):
        return obj.active_state.name

    get_log_id.short_description = 'Log ID'
    get_option_id.short_description = 'Option ID'
    get_option_name.short_description = 'Option Name'
    get_active_state.short_description = 'Active State'


class XabslSymbolAdmin(admin.ModelAdmin):
    list_display = ('get_log_id', 'frame', 'symbol_type','symbol_name', 'symbol_value')

    def get_log_id(self, obj):
        return obj.log_id.id
    
# Register your models here.
admin.site.register(Event)
admin.site.register(Game, GameAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(CognitionRepresentation, CognitionRepresentationAdmin)
admin.site.register(MotionRepresentation)
admin.site.register(BehaviorOption, BehaviorOptionAdmin)
admin.site.register(BehaviorOptionState, BehaviorOptionStateAdmin)
admin.site.register(BehaviorFrameOption, BehaviorFrameOptionAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(XabslSymbol, XabslSymbolAdmin)