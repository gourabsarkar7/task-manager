"""Comments Models"""
from datetime import datetime
from coreapi import Field
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.forms import FileField
import django

from user_auth.models import UserModel


# Create your models here.
class CommentModel(models.Model):
    """Model for comments module."""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    comment_user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True,related_name='comment_user')
    # task_id = models.CharField(max_length=50,blank=True)
    description = models.CharField(max_length=300, default="", blank=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()
    files = ArrayField(models.FileField(max_length=200,blank=True),blank=True,default=list,max_length=5)

    def __str__(self):
         return f"{self.description}"

    