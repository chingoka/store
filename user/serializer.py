from rest_framework import serializers
from django.contrib.auth import  authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['firstName', 'middleName', 'lastName', 'username', 'phoneNumber', 'email', 'role', 'password', 'email_token']

    def validate(self, data):
        try:
            user=User(**data)
            user.full_clean()
        except Exception as e:
            raise serializers.ValidationError(e)
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.is_verified = False  # Initially set to unverified
        user.save()
        return user

 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError("Incorrect Credentials")

        if not user.is_active:
            raise serializers.ValidationError("User is not active")
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        if not check_password(data['current_password'], user.password):
            raise serializers.ValidationError({"current_password": "Incorrect current password"})

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match"})

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)