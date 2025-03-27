from django.urls import path
from .views import CategorySizeStoreView, ProductCreateView, ProductListAPIView
app_name = 'product'
urlpatterns = [
    path('category_size/', CategorySizeStoreView.as_view(), name='category-size-store'),
    path('add/', ProductCreateView.as_view(), name='product-add'),
    path('list/', ProductListAPIView.as_view(), name='product-list'),
]
