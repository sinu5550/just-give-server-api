from rest_framework import serializers
from . import models

class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gift
        fields = '__all__'