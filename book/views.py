from django.shortcuts import render
from rest_framework import viewsets,filters
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication
# Create your views here.
class BooksWithSpecificUser(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user_id = request.query_params.get("user_id")
        if user_id:
            return queryset.filter(user=user_id)
        return queryset
    
class BookViewset(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    filter_backends = [BooksWithSpecificUser]

    
