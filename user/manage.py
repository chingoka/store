from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def email_validator(self,email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("please enter the valid email address"))
        
        
    def create_user(self, username, email=None, phoneNumber=None, password=None, **extra_fields):
        """
        Creates and saves a regular User with the given email, phone number, and password.
        """
        if not username:
            raise ValueError("Users must have a username")

        # Create the user model
        user = self.model(
            username=username,
            phoneNumber=phoneNumber,
            email=self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, phoneNumber=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, phone number, and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        return self.create_user(
            username=username,
            phoneNumber=phoneNumber,
            password=password,
            email=email,
            **extra_fields,
        )
