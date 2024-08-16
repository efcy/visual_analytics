from rest_framework import serializers
from .models import vat_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = vat_user
        fields = '__all__'