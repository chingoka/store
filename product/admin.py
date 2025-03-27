from django.contrib import admin
from product.models import Category, Product, ProductTransfer, Receipt, Size

# Customize Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category__name', 'quantity', 'size__name', 'store', 'user', 'timestamp')
    search_fields = ('name', 'category')  
    list_filter = ('store', 'category')  

# Customize ProductTransfer Admin
class ProductTransferAdmin(admin.ModelAdmin):
    list_display = ('product__name',  'store', 'shop_name', 'user', 'transfer_date')
    search_fields = ('product__name',  'store', 'shop_name') 
    list_filter = ('store','shop_name') 

# Customize Receipt Admin
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'query', 'created_at')
    search_fields = ('user__email', 'query')  
    list_filter = ('created_at',)  

class CategoriesAdmin(admin.ModelAdmin):
    list_display=('id','name','added_at')

class SizeAdmin(admin.ModelAdmin):
    list_display=('id','name','added_at')
   

# Register models with custom admin
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductTransfer, ProductTransferAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Category, CategoriesAdmin)
admin.site.register(Size, SizeAdmin)



