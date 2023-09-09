"""Project Models"""
from datetime import datetime
from django.db import models
import django

from user_auth.models import UserModel

class ProjectStatusModel(models.Model):
    """Class for project status model"""
    id = models.AutoField(primary_key=True)
    project_status = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
         return f"{self.project_status}"

# Create your models here.
class ProjectModel(models.Model):
    """Class for project model"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    color = models.CharField(max_length=50, default="", blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, default="", blank=True)
    status = models.ForeignKey(ProjectStatusModel, on_delete=models.CASCADE,null=True,blank=True,default='',related_name='project_status_id')
    duration = models.DurationField()
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    archive = models.BooleanField(default=False, blank=True)
    objects = models.Manager()

    def __str__(self):
         return f"{self.name}"


class ProjectAssigneeModel(models.Model):
    """Class for project assignee model"""
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE,null=True)
    assignee_ids = models.CharField(max_length=50)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True,blank=True,default='',related_name='user_id')
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
         return f"{self.project}"
