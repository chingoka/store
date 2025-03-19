from django.contrib import admin

# Register your models here.
from django.contrib import admin

from store.models import StoreProduct, Store

# Customize Stores Admin
class StoresAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)  
    

class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('store','quantity', 'size')
    search_fields = ('store','product')


    
admin.site.register(Store, StoresAdmin)
admin.site.register(StoreProduct, StoreProductAdmin)