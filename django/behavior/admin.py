
from django.contrib import admin
from .models import BehaviorOption, BehaviorOptionState, BehaviorFrameOption, XabslSymbolSparse, XabslSymbolComplete

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

class XabslSymbolCompleteAdmin(admin.ModelAdmin):
    list_display = ["get_log_id"]

    def get_log_id(self, obj):
        return obj.log_id.id
    
    get_log_id.short_description = 'Log ID'


#class XabslSymbolAdmin(admin.ModelAdmin):
#    list_display = ('get_log_id', 'frame', 'symbol_type','symbol_name', 'symbol_value')
#    search_fields = ['log_id__id', 'symbol_name', 'frame']
#    def get_log_id(self, obj):
#        return obj.log_id.id


admin.site.register(BehaviorOption)
admin.site.register(BehaviorOptionState)
admin.site.register(BehaviorFrameOption, BehaviorFrameOptionAdmin)
admin.site.register(XabslSymbolComplete, XabslSymbolCompleteAdmin)
admin.site.register(XabslSymbolSparse)
