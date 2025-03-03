from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    CognitionFrame,
    FrameFilter,
    BallModel,
    BallCandidates,
    BallCandidatesTop,
    CameraMatrix,
    CameraMatrixTop,
    OdometryData,
    FieldPercept,
    FieldPerceptTop,
    GoalPercept,
    GoalPerceptTop,
    MultiBallPercept,
    RansacLinePercept,
    ShortLinePercept,
    ScanLineEdgelPercept,
    ScanLineEdgelPerceptTop,
    RansacCirclePercept2018,
)

class CognitionFrameAdmin(ModelAdmin):
    list_display = ("get_log_id", "get_frame_id", "frame_number")

    def get_log_id(self, obj):
        return obj.log.id
    
    def get_frame_id(self, obj):
        return obj.id

    get_log_id.short_description = "Log ID"
    get_frame_id.short_description = "Frame ID"


class FrameFilterAdmin(ModelAdmin):
    list_display = ("get_log_id", "get_user")

    def get_log_id(self, obj):
        return obj.log.id

    def get_user(self, obj):
        return obj.user

    get_log_id.short_description = "Log ID"


class BallModelAdmin(ModelAdmin):
    list_display = ("get_id", "get_log_id", "get_frame_number")

    def get_log_id(self, obj):
        return obj.frame.log_id

    def get_frame_number(self, obj):
        return obj.frame.frame_number

    def get_id(self, obj):
        return obj.id


admin.site.register(CognitionFrame, CognitionFrameAdmin)
admin.site.register(FrameFilter, FrameFilterAdmin)
admin.site.register(BallModel, BallModelAdmin)
admin.site.register(BallCandidates)
admin.site.register(BallCandidatesTop)
admin.site.register(CameraMatrix)
admin.site.register(CameraMatrixTop)
admin.site.register(OdometryData)
admin.site.register(FieldPercept)
admin.site.register(FieldPerceptTop)
admin.site.register(GoalPercept)
admin.site.register(GoalPerceptTop)
admin.site.register(MultiBallPercept)
admin.site.register(RansacLinePercept)
admin.site.register(ShortLinePercept)
admin.site.register(ScanLineEdgelPercept)
admin.site.register(ScanLineEdgelPerceptTop)
admin.site.register(RansacCirclePercept2018)
