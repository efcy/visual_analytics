from graphene_django import DjangoObjectType
from .. import models

class EventType(DjangoObjectType):
    class Meta:
        model = models.Event
        fields = "__all__"

class GameType(DjangoObjectType):
    class Meta:
        model = models.Game
        fields = "__all__"

class LogType(DjangoObjectType):
    class Meta:
        model = models.Log
        fields = "__all__"

class VideoRecordingType(DjangoObjectType):
    class Meta:
        model = models.VideoRecording
        fields = "__all__"


class ExperimentType(DjangoObjectType):
    class Meta:
        model = models.Experiment
        fields = "__all__"

class LogStatusType(DjangoObjectType):
    class Meta:
        model = models.LogStatus
        fields = "__all__"

class CognitionFrameType(DjangoObjectType):
    class Meta:
        model = models.CognitionFrame
        fields = "__all__"


class MotionFrameType(DjangoObjectType):
    class Meta:
        model = models.MotionFrame
        fields = "__all__"

class ImageType(DjangoObjectType):
    class Meta:
        model = models.Image
        fields = "__all__"

class AnnotationType(DjangoObjectType):
    class Meta:
        model = models.Annotation
        fields = "__all__"


class CognitionRepresentationType(DjangoObjectType):
    class Meta:
        model = models.CognitionRepresentation
        fields = "__all__"

class MotionRepresentationType(DjangoObjectType):
    class Meta:
        model = models.MotionRepresentation
        fields = "__all__"

class BehaviorOptionStateType(DjangoObjectType):
    class Meta:
        model = models.BehaviorOptionState
        fields = "__all__"

class BehaviorFrameOptionType(DjangoObjectType):
    class Meta:
        model = models.BehaviorFrameOption
        fields = "__all__"

class XabslSymbolCompleteType(DjangoObjectType):
    class Meta:
        model = models.XabslSymbolComplete
        fields = "__all__"

class XabslSymbolSparseType(DjangoObjectType):
    class Meta:
        model = models.XabslSymbolSparse
        fields = "__all__"

class FrameFilterType(DjangoObjectType):
    class Meta:
        model = models.FrameFilter
        fields = "__all__"
