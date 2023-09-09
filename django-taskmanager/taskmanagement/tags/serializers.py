"""Serializer for tag module"""
from rest_framework import serializers
from tags.models import TagModel


class AddTagSerializer(serializers.ModelSerializer):
    """Serializer to add tags"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TagModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete", "user"]


class UpdateTagSerializer(serializers.ModelSerializer):
    """Serializer to update tags"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TagModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete", "user"]


class DeleteTagSerializer(serializers.ModelSerializer):
    """Serializer to delete tags"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TagModel
        fields = ['id']


class GetTagSerializer(serializers.ModelSerializer):
    """Serializer to get tags"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = TagModel
        fields = ['task', 'id']
