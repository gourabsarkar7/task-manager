"""Notes Models"""
from datetime import datetime
from django.db import models

import django

from user_auth.models import UserModel

# Create your models here.
class NotesModel(models.Model):
    """Class for Note model"""
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300, default="", blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()
    
    def __str__(self):
         return f"{self.title}"
