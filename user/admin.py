from django.contrib import admin

from user.models import User

# Customize User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstName', 'middleName', 'lastName', 'username', 'phoneNumber', 'is_verified', 'is_active', 'is_staff', 'role')
    search_fields = ('email', 'firstName', 'middleName', 'lastName', 'username', 'phoneNumber')  
    list_filter = ('is_active', 'is_staff', 'is_verified', 'role')  

admin.site.register(User, UserAdmin)
