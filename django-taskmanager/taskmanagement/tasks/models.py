"""Task module"""
import datetime
from pickle import FALSE
import django
from django.db import models

from projects.models import ProjectModel
from user_auth.models import UserModel

# Create your models here.

class TaskPriorityModel(models.Model):
    """Model for task priority"""
    id = models.AutoField(primary_key=True)
    task_priority = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.task_priority}"

testeddate = '23/04/2015'
class TaskModel(models.Model):
    """Class for Task model"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True)
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=50, blank=True, default="")
    description = models.CharField(max_length=300, default="", blank=True)
    isCompleted = models.BooleanField(max_length=200, blank=True, default=False,null=True)
    priority = models.ForeignKey(TaskPriorityModel, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    tag_id = models.CharField(max_length=20, blank=True, default="")
    reviewer = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name='reviewer_id',null=True,default="")
    assignee = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name='assignee_id',null=True,default="")
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"
    


class TaskStatusModel(models.Model):
    """Model for task status"""
    id = models.AutoField(primary_key=True)
    task_status = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.task_status}"
