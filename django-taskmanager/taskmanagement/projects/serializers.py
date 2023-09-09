
"""Serializers for project module"""
from rest_framework import serializers
from projects.models import ProjectAssigneeModel, ProjectModel, ProjectStatusModel


class AddProjectSerializer(serializers.ModelSerializer):
    """Serializer for adding project"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectModel
        exclude = ["created_at", "updated_at", "is_active",
                   "is_delete", "status", "user"]


class UpdateProjectSerializer(serializers.ModelSerializer):
    """Serializer for updating project"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete", "user"]


class GetProjectSerializer(serializers.ModelSerializer):
    """Serializer for getting project"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectModel
        fields = ['id']


class DeleteProjectSerializer(serializers.ModelSerializer):
    """Serializer for deleting project"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectModel
        fields = ['id']


class AddProjectStatusSerializer(serializers.ModelSerializer):
    """Serializer for adding project status"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectStatusModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class GetProjectStatusSerializer(serializers.ModelSerializer):
    """Serializer for getting project status"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectStatusModel
        exclude = ["project_status", "created_at",
                   "updated_at", "is_active", "is_delete"]


class UpdateProjectStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating project status"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectStatusModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class DeleteProjectStatusSerializer(serializers.ModelSerializer):
    """Serializer for deleting project status"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectStatusModel
        exclude = ["project_status", "created_at",
                   "updated_at", "is_active", "is_delete"]


class AddProjectAssigneeSerializer(serializers.ModelSerializer):
    """Serializer for adding project assignees"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectAssigneeModel
        exclude = ["user", "created_at",
                   "updated_at", "is_active", "is_delete"]


class DeleteProjectAssigneeSerializer(serializers.ModelSerializer):
    """Serializer for deleting project assignees"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectAssigneeModel
        exclude = ["user", "created_at",
                   "updated_at", "is_active", "is_delete"]


class GetProjectAssigneeSerializer(serializers.ModelSerializer):
    """Serializer for getting project assignees"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectAssigneeModel
        exclude = ["user", "assignee_ids", "created_at",
                   "updated_at", "is_active", "is_delete"]


class InviteProjectAssigneeSerializer(serializers.ModelSerializer):
    """Serializer for adding project assignees"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ProjectAssigneeModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete", "user"]
