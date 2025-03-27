from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('user/', include('user.urls')),
    path('product/',include('product.urls')),
    path('document/',include('document.urls')),
   
]
