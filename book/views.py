from django.shortcuts import render
from rest_framework import viewsets,filters
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
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

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Book listed for donation successfully.'}, status=status.HTTP_201_CREATED)
    
