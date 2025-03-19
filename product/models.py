from django.db import models
from store.models import Store
from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Category Name')
    added_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Size Name')
    added_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Product Name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Size')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Store')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Times stored')

    def __str__(self):
        return f'{self.name} ({self.category.name}, {self.size.name})'

class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    query = models.TextField(blank=True, null=True, verbose_name='Query')
    image = models.ImageField(upload_to='receipts/', blank=True, null=True, verbose_name='Receipt Image')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def __str__(self):
        return f"Receipt by {self.user.username} - ${self.amount}"

class ProductTransfer(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='From Store')
    shop_name = models.CharField(max_length=100, verbose_name='To Shop Name')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    transfer_date = models.DateTimeField(auto_now_add=True, verbose_name='Transfer Date')

    def __str__(self):
        return f"{self.product.name} transferred from {self.store.name} to {self.shop_name}"
