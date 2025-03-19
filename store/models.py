from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_products')
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_products')
    quantity = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=50, choices=[('set', 'Set'), ('box', 'Box'), ('bandru', 'Bandru')])
    created_at =models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # unique_together = ('store', 'product')
        unique_together = ('store', 'size')
    
    def reduce_quantity(self, amount):
        """ Reduces product quantity in the store. """
        if amount > self.quantity:
            raise ValueError("Not enough stock available")
        self.quantity -= amount
        self.save()
    
    # def __str__(self):
        # return f"{self.product.name} in {self.store.name} - {self.quantity} left"