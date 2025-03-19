import uuid
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from user.manage import MyUserManager

from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver



class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=30, null=True, blank=True)
    middleName = models.CharField(max_length=30, null=True, blank=True)
    lastName = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(verbose_name='username', unique=True, max_length=200)
    phoneNumber = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    email_token = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin'),        
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')

    reset_token =None
    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['phoneNumber', 'email']

    def __str__(self):
        return self.username

    @property
    def id(self):
       return self.user_id

    @property
    def get_full_name(self):
        return f"{self.firstName} {self.lastName}"
    
    @classmethod
    def get_user_by_email(cls,email: str) -> 'User':
        return cls.objects.filter(email=email).first()


@receiver(post_save, sender =settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
