from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db import IntegrityError
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

class SensorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SensorLog
        fields = '__all__'


class ImageAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageAnnotation
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'

class RobotDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RobotData
        fields = '__all__'


    def create(self, validated_data):
        # TODO figure out why this works
        instance, created = models.RobotData.objects.get_or_create(
            game=validated_data.get('game'),
            player_number=validated_data.get('player_number'),
            head_number=validated_data.get('head_number'),
            log_path=validated_data.get('log_path'),
            defaults=validated_data
        )
        return instance



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = '__all__'
        # FIXME adding __all__ is bad practice, explicitely say what we send










