from rest_framework import serializers
from . import models

class BookSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Book
        fields = '__all__'