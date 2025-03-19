from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse

from product.models import Product

# # Create your views here.


@api_view(['GET'])
def getEndpoint(request):
    base_url = request.build_absolute_uri('/')[:-1]
     # Get a product if available
    # product = Product.objects.first()
    # product_url = base_url + reverse('product:product-update', kwargs={'pk': product.pk}) if product else "No products available"
    # product_urls = base_url + reverse('product:product-delete', kwargs={'pk': product.pk}) if product else "No products available"
    url = [
        {
            'appName':'user',
            'urls':[
                 {
                    'endpoint':base_url + reverse('user:auth'),
                    'description':'user login'
                },
                 {
                    'endpoint':base_url + reverse('user:registration'),
                    'description':'user registration'
                },
                  {
                    'endpoint':base_url + reverse('user:user-detail'),
                    'description':'detail of user'
                },
                  {
                    'endpoint':base_url + reverse('user:change-password'),
                    'description':'change password'
                },
                   {
                    'endpoint':base_url + reverse('user:verify-email'),
                    'description':'verify email'
                },
            ],

        },
        {
            'appName': 'product',
            'urls': [
                {
                    'endpoint': base_url + reverse('product:product-list'),
                    'description': 'product list'
                },
                {
                    'endpoint': base_url + reverse('product:product-add'),
                    'description': 'add product'
                },
                # {
                #     'endpoint': base_url + reverse('product:product-create'),
                #     'description': 'create product'
                # },
                {
                    'endpoint': base_url + reverse('product:category-size-store'),
                    'description': 'create product'
                },
                #    {
                #     'endpoint': product_url,
                #     'description': 'product update'
                # },
                #     {
                #     'endpoint': product_urls,
                #     'description': 'product delete'
                # },
            ]
        },
                {
            'appName': 'document',
            'urls': [
                {
                    'endpoint': base_url + reverse('document:document-list'),
                    'description': 'document list'
                },
                {
                    'endpoint': base_url + reverse('document:document-detail'),
                    'description': 'document detail'
                },

            ]
        },
       
        {
            'appName': 'Admin',
            'urls': [
                {
                    'endpoint': base_url + reverse('admin:index'),
                    'description': 'admin page'
                },
            ]
        }


    ]
    return Response(url)