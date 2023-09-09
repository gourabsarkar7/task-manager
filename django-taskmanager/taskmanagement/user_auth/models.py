"""Serializer for usermodel"""

from datetime import datetime
from django import forms
from django.db import models
from django.forms import ModelForm
from phonenumber_field.modelfields import PhoneNumberField
import django


# Create your models here.

class UserStatusModel(models.Model):
    """Serializer for user status"""
    id = models.AutoField(primary_key=True)
    user_status = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.user_status}"

class UserRoleModel(models.Model):
    """Serializer for user role"""
    id = models.AutoField(primary_key=True)
    user_role = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.user_role}"

class UserModel(models.Model):
    """Serializer for user model"""
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    # user_id = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50)
    status = models.ForeignKey(UserStatusModel, on_delete=models.CASCADE,null=True)
    profile_pic = models.FileField(blank=True)
    email = models.EmailField()
    mobile_number = PhoneNumberField()
    password = models.CharField(max_length=20,null=True)
    role = models.ForeignKey(UserRoleModel, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
         return f"{self.first_name} {self.last_name}"

class OtpForPasswordModel(models.Model):
    """Serializer for user status"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    otp = models.IntegerField()
