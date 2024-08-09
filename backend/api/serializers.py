from django.contrib.auth.models import User
from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class FrameTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FrameTime
        fields = '__all__'

class SensorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SensorLog
        fields = ['sensor_frame_number']


class ImageAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageAnnotation
        fields = '__all__'

class CameraMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CameraMatrix
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    #event = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    event = EventSerializer()
    class Meta:
        model = models.Game
        fields = '__all__'
        # FIXME adding __all__ is bad practice, explicitely say what we send










