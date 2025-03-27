from django.contrib import admin

from document.models import Documents

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display=('title','amount','description','sender')
    search_fields=('title','sender','amount')
    
admin.site.register(Documents,DocumentAdmin)