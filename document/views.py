from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.response import Response

from document.models import Documents
from document.serializer import DocumentSerializer

# Create your views here.

class DocumentCreatApiView(generics.CreateAPIView):
    queryset=Documents.objects.all()
    serializer_class =DocumentSerializer
    permission_classes =[permissions.AllowAny]
    
    
    def perform_create(self, serializer):
      serializer.save(user=self.request.user)

# class for list document
class DocumentListAPIView(generics.ListAPIView):
    serializer_class=DocumentSerializer
    queryset=Documents.objects.all()
    permission_classes=[permissions.AllowAny]
    
    def list(self,request):
        queryset=self.get_queryset()
        serializer = DocumentSerializer(queryset,many=True)
        return Response(serializer.data)