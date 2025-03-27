from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
import json
from rest_framework_simplejwt.tokens import RefreshToken

from store.models import StoreProduct, Stores
from store.serializer import StoreProductSerializer, StoreSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Stores.objects.all()
    serializer_class = StoreSerializer
    


class StoreProductViewSet(viewsets.ModelViewSet):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer

    @action(detail=True, methods=['post'])
    def reduce_stock(self, request, pk=None):
        store_product = self.get_object()
        amount = int(request.data.get('amount', 0))
        
        try:
            store_product.reduce_quantity(amount)
            return Response({'message': 'Stock reduced successfully'})
        except ValueError as e:
            return Response({'error': str(e)}, status=400)