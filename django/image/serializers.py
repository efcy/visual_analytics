from rest_framework import serializers
from .models import NaoImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaoImage
        fields = "__all__"
