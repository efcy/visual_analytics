from rest_framework import serializers
from .models import MotionFrame


class MotionFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotionFrame
        fields = "__all__"
