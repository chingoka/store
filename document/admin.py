from django.contrib import admin

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display=('title','amount','description','sender')
    search_fields=('title','sender','amount')