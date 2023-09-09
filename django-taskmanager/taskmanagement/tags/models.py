"""Tag Model class"""
from datetime import datetime
from django.db import models
import django
from tasks.models import TaskModel

from user_auth.models import UserModel

# Create your models here.


class TagModel(models.Model):
    """Class for tag model"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE,null=True,related_name='task_id')
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
         return f"{self.name}"
