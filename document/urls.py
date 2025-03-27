from django.urls import path
from .views import DocumentCreatApiView, DocumentListAPIView

app_name = 'document'
urlpatterns=[
    path('document-add/', DocumentCreatApiView.as_view(),name='document-add'),
    path('document-list/', DocumentListAPIView.as_view(),name='document-list'),
]

