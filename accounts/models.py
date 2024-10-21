from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import models
from django.contrib.auth.models import User


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# models.py
from django.db import models

from django.conf import settings
from django.http import JsonResponse
class Appliance(models.Model):
    appliance_type = models.CharField(max_length=100)
    details = models.TextField()
    photo = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.appliance_type
from .models import Appliance
def upload_appliance(request):
    if request.method == 'POST':
        appliance_type = request.POST.get('appliance_type')
        details = request.POST.get('details')
        photo = request.FILES.get('photo')

        if not appliance_type or not details or not photo:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        # Save the data to the database
        appliance = Appliance.objects.create(
            appliance_type=appliance_type,
            details=details,
            photo=photo
        )

        # Return the response with the file URL
        return JsonResponse({
            'message': 'Upload successful',
            'file_url': appliance.photo.url,
            'appliance_type': appliance.appliance_type,
            'details': appliance.details
        }, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)
