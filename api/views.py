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
                #  {
                #     'endpoint':base_url + reverse('user:api/token-auth/'),
                #     'description':'user token-auth'
                # },
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
                    'endpoint': base_url + reverse('document:document-add'),
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