import uuid
import json
from typing import Any

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from rest_framework import generics, permissions, status, authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from itsdangerous import URLSafeTimedSerializer

from ChingokaSystem import settings
from user.models import User
from user.serializer import (
    LoginSerializer, RegisterUserSerializer, EmailVerificationSerializer,
    ChangePasswordSerializer, ResetPasswordSerializer, UserSerializer
)
from user.utils import send_verification_email

class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        token = str(uuid.uuid4())
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        try:
            with transaction.atomic():
                serializer.save(email_token=token)

                send_verification_email(email=validated_data.get("email"))
                
            return Response({'message': 'User registered. Check your email to activate your account.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # logger.error(f"Error during user registration: {str(e)}")
            return Response({'message': f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication, JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = RefreshToken.for_user(user)
        role_redirect = {
            "admin": "/admin",
            "organizer": "/organizer-dashboard",
            "employee": "/attendee-dashboard",
        }
        redirect_url = role_redirect.get(getattr(user, "role", "attendee"), "/")

        data = {
            "refresh": str(token),
            "access": str(token.access_token),
            "role": getattr(user, "role", "attendee"),
            "redirect_url": redirect_url,
            "user": UserSerializer(user).data,
        }
        return Response(data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class ValidateUserView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse({"valid": False, "error": "Email is required"}, status=400)

        user_exists = User.objects.filter(email=email).exists()
        return JsonResponse({"valid": user_exists})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get("token")
        
        if not token:
            return Response({'message': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
        
        try:
            email = serializer.loads(token, max_age=3600)  # Token expires in 1 hour
            user = User.objects.get(email=email)
            user.is_active = True
            user.is_verified = True
            user.save()
            
            return Response({'message': 'Email successfully verified!',
                             "redirect_url": f"{settings.FRONTEND_BASE_URL}login"},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'Invalid or expired token: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # logger.info(f'Login attempt with data: username={username}')

        # Check for missing data
        if not username or not password:
            # logger.warning('Login attempt failed: Missing username or password')
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({
                "error": "The username provided does not exist. Please check your username.",
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is None:
            # logger.warning(f'Authentication failed for username: {username}')
            return Response({'error': 'The password provided is incorrect. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            # logger.warning(f'User {username} is inactive')
            return Response({'error': 'User is inactive'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate token
        token, _ = Token.objects.get_or_create(user=user)
        role = user.role
        firstName = user.firstName
        middleName = user.middleName
        user_id = user.user_id

        # logger.info(f'Successful login for user: {username}, Role: {role}')

        return Response({
            'token': token.key,
            'role': role,
            'firstName': firstName,
            'middleName': middleName,
            'username': username,
            'user_id': user_id
        }, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data.get("new_password"))
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes =[permissions.AllowAny]
    
    def list(self, request):
        role = request.query_params.get("role")
        if role:
            queryset = self.get_queryset().filter(role=role)  # Filter by category
        else:
            queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)