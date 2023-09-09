"""Serializers for comment module"""
from rest_framework import serializers

from checklist.models import ChecklistModel,ChecklistDetailModel


class AddChecklistSerializer(serializers.ModelSerializer):
    """Serializers for adding checklist"""
    
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChecklistModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete","user"]

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChecklistDetailModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete","user","checklist"]

class UpdateChecklistSerializer(serializers.ModelSerializer):
    """Serializers for updating checklist"""
    id = serializers.IntegerField()
    title = serializers.CharField(default=None)
    color = serializers.CharField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChecklistModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete","user"]

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChecklistDetailModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete","user","checklist"]


class DeleteChecklistSerializer(serializers.ModelSerializer):
    """Serializers for deleting checklist"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChecklistModel
        fields = ['id']

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChecklistDetailModel
        fields = ['id']


class GetChecklistSerializer(serializers.ModelSerializer):
    """Serializers for getting checklist"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChecklistModel
        fields = ['id']

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = ChecklistDetailModel
        fields = ['id']
