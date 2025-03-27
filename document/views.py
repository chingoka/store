from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication

from document.models import Documents
from document.serializer import DocumentListUserSerializer, DocumentSerializer

# Create your views here.

class DocumentCreatApiView(generics.CreateAPIView):
    queryset=Documents.objects.all()
    serializer_class =DocumentSerializer
    permission_classes = [AllowAny]
    

# class for list document
class DocumentListAPIView(generics.ListAPIView):
    serializer_class=DocumentListUserSerializer
    queryset=Documents.objects.all()
    permission_classes=[permissions.AllowAny]
    
    def list(self,request):
        queryset=self.get_queryset()
        serializer = DocumentSerializer(queryset,many=True)
        return Response(serializer.data)