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


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Annotation
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
    class Meta:
        model = models.Game
        fields = '__all__'


class CognitionRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CognitionRepresentation
        fields = '__all__'


class MotionRepresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MotionRepresentation
        fields = '__all__'


class BehaviorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorOption
        fields = '__all__'


class BehaviorOptionsStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorOptionState
        fields = '__all__'

class BehaviorFrameOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BehaviorFrameOption
        fields = '__all__'