from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
class BookSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False, required=False)
    class Meta:
        model = models.Book
        fields = '__all__'