"""Module for task serializer"""
from rest_framework import serializers
from tasks.models import TaskModel, TaskStatusModel , TaskPriorityModel


class AddTaskSerializer(serializers.ModelSerializer):
    """Serializer for adding task"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskModel
        exclude = ["created_at", "updated_at", "is_active",
                   "is_delete", "isCompleted", "user"]


class UpdateTaskSerializer(serializers.ModelSerializer):
    """Serializer for updating task"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete", "user"]


class DeleteTaskSerializer(serializers.ModelSerializer):
    """Serializer for deleting task"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskModel
        fields = ['id']


class GetTaskSerializer(serializers.ModelSerializer):
    """Serializer for getting task"""
    # id = serializers.IntegerField(default=None)
    # project_id = serializers.CharField(max_length=50,default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskModel
        fields = ["isCompleted"]


class AddTaskStatusSerializer(serializers.ModelSerializer):
    """Serializer for adding task status"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskStatusModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class GetTaskStatusSerializer(serializers.ModelSerializer):
    """Serializer for getting task status"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskStatusModel
        exclude = ["isCompleted", "created_at",
                   "updated_at", "is_active", "is_delete"]


class UpdateTaskStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating task status"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskStatusModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class DeleteTaskStatusSerializer(serializers.ModelSerializer):
    """Serializer for deleting task status"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskStatusModel
        exclude = ["isCompleted", "created_at",
                   "updated_at", "is_active", "is_delete"]


class AddTaskPrioritySerializer(serializers.ModelSerializer):
    """Serializer for adding task status"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskPriorityModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class GetTaskPrioritySerializer(serializers.ModelSerializer):
    """Serializer for getting task status"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskPriorityModel
        exclude = ["isCompleted", "created_at",
                   "updated_at", "is_active", "is_delete"]


class UpdateTaskPrioritySerializer(serializers.ModelSerializer):
    """Serializer for updating task status"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskPriorityModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class DeleteTaskPrioritySerializer(serializers.ModelSerializer):
    """Serializer for deleting task status"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TaskPriorityModel
        exclude = ["isCompleted", "created_at",
                   "updated_at", "is_active", "is_delete"]