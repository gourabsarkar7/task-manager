"""Serializers for notes module"""
from rest_framework import serializers
from notes.models import NotesModel


class AddNoteSerializer(serializers.ModelSerializer):
    """Serializers for adding notes"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = NotesModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete", "user"]


class UpdateNoteSerializer(serializers.ModelSerializer):
    """Serializers for updating notes"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = NotesModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete", "user"]


class DeleteNoteSerializer(serializers.ModelSerializer):
    """Serializers for deleting notes"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = NotesModel
        fields = ['id']


class GetNoteSerializer(serializers.ModelSerializer):
    """Serializers for getting notes"""
    # id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = NotesModel
        fields = []
