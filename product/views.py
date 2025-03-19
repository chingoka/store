import logging
from rest_framework.views import APIView
from rest_framework import generics, permissions, status, authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from store.models import Store
from store.serializer import StoreSerializer
from .models import Category, Product, ProductTransfer, Receipt, Size
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializer import ProductSerializer, CategorySerializer, ProductViewSerializer, SizeSerializer, StoreSerializer

# Configure logging
logger = logging.getLogger(__name__)

# Fetch Categories, Sizes, and Stores
class CategorySizeStoreView(ListAPIView):
    def get_queryset(self):
        logger.info("Fetching categories, sizes, and stores")
        return {"categories": Category.objects.all(), "sizes": Size.objects.all(), "store": Store.objects.all()}

    def list(self, request, *args, **kwargs):
        logger.info("Listing categories, sizes, and stores")
        return Response({
            "categories": CategorySerializer(Category.objects.all(), many=True).data,
            "sizes": SizeSerializer(Size.objects.all(), many=True).data,
            "store": StoreSerializer(Store.objects.all(), many=True).data
        })

# Create Products
class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        logger.info("Received product creation request")
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Product created successfully: {response.data}")
            return response
        except ValidationError as e:
            logger.error(f"Validation error while creating product: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.critical(f"Unexpected error during product creation: {e}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductListAPIView(ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductViewSerializer
    permission_classes= [permissions.AllowAny]
    