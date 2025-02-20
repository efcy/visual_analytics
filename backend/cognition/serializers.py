from rest_framework import serializers
from .models import CognitionFrame


class CognitionFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CognitionFrame
        fields = '__all__'