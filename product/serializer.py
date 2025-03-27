
from rest_framework import serializers
from .models import Product, Category, Size, Store

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"


class ProductViewSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    size = serializers.CharField(source="size.name", read_only=True)
    store = serializers.CharField(source="store.name", read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = Product
        fields = ["id", "name", "category", "quantity", "size", "store","user", "timestamp"]
