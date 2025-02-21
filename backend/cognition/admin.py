from django.contrib import admin
from .models import *


admin.site.register(CognitionFrame)
admin.site.register(BallModel)

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