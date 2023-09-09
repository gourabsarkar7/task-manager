"""Serializer for user module"""

from rest_framework import serializers
from django.contrib.auth import password_validation
from jwt_utility import JWTUtility
from .models import UserModel, UserRoleModel, UserStatusModel


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User details"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        exclude = ["created_at",
                   "updated_at", "is_active", "is_delete", "status"]
    
    def validate_password(self, value):
        """Function for password validation"""
        password_validation.validate_password(value, self.instance)
        return value
    
    @staticmethod
    def get_token(user):
        """Function to get user token"""
        return JWTUtility.encode_token(user)


class SignInSerializer(serializers.ModelSerializer):
    """Serializer for user sign in"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ['email', 'password']
    
    @staticmethod
    def get_token(user):
        """Function to get user token"""
        return JWTUtility.encode_token(user)


class ForgotPasswordSerializer(serializers.ModelSerializer):
    """Serializer for forget password"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ['email']


class ResetPasswordSerializer(serializers.ModelSerializer):
    """Serializer for reset password"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ['password']


class UserUpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        exclude = ["created_at",
                   "updated_at", "is_active", "is_delete","password","email","mobile_number"]


class DeleteProfileSerializer(serializers.ModelSerializer):
    """Serializer for deleting user profile"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ['id']


class AddUserStatusSerializer(serializers.ModelSerializer):
    """Serializer for adding user role"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserStatusModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class GetUserStatusSerializer(serializers.ModelSerializer):
    """Serializer for getting user role"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserStatusModel
        exclude = ["user_status", "created_at",
                   "updated_at", "is_active", "is_delete"]


class UpdateUserStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating user role"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserStatusModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class DeleteUserStatusSerializer(serializers.ModelSerializer):
    """Serializer for deleting user role"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserStatusModel
        exclude = ["user_status", "created_at",
                   "updated_at", "is_active", "is_delete"]


class AddUserRoleSerializer(serializers.ModelSerializer):
    """Serializer for adding user role"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserRoleModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class GetUserRoleSerializer(serializers.ModelSerializer):
    """Serializer for getting user role"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserRoleModel
        exclude = ["user_role", "created_at",
                   "updated_at", "is_active", "is_delete"]


class UpdateUserRoleSerializer(serializers.ModelSerializer):
    """Serializer for updating user role"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserRoleModel
        exclude = ["created_at", "updated_at", "is_active", "is_delete"]


class DeleteUserRoleSerializer(serializers.ModelSerializer):
    """Serializer for deleting user role"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserRoleModel
        exclude = ["user_role", "created_at",
                   "updated_at", "is_active", "is_delete"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer for changing password"""
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = ['old_password', 'new_password']

    def validate_password(self, value):
        """function for validating password"""
        password_validation.validate_password(value, self.instance)
        return value


class RefreshAuthTokenSerializer(serializers.ModelSerializer):
    """Serializer for refreshing token for a user"""

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = []

    @staticmethod
    def get_token(user):
        """Function to get user token"""
        return JWTUtility.encode_refresh_token(user)

# class LogoutUserSerializer(serializers.ModelSerializer):
#     """Serializer for logging out the user and expiring that particular token"""
#     class Meta:
#         """Meta class to change behaviour of model fields"""
#         model = UserModel
#         fields = []

class GetAllUsersSerializer(serializers.ModelSerializer):
    """Serializer for getting user role"""

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = UserModel
        fields = []