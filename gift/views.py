from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
# Create your views here.
class GiftViewset(viewsets.ModelViewSet):
    queryset = models.Gift.objects.all()
    serializer_class = serializers.GiftSerializer