from rest_framework import serializers
from .models import VATUser


class VATUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VATUser
        fields = "__all__"
