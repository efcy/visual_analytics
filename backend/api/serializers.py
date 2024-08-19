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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("RobotDataSerializer initialized")

    def to_internal_value(self, data):
        print(f"to_internal_value called with data: {data}")
        return super().to_internal_value(data)
    
    def is_valid(self, raise_exception=False):
        valid = super().is_valid(raise_exception=False)
        if not valid:
            print(f"Serializer errors: {self.errors}")
        return True

    def validate(self, attrs):
        print("run validate")
        # Check if an object with these unique fields already exists
        

    def create(self, validated_data):
        # If we get here, we know the object doesn't exist, so we can create it
        return super().create(validated_data)



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = '__all__'
        # FIXME adding __all__ is bad practice, explicitely say what we send










