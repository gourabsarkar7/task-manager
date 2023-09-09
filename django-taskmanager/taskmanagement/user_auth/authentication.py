"""Class for token authentication"""

from rest_framework import authentication
from rest_framework import exceptions
from jwt_utility import JWTUtility
from .models import UserModel
from response import Response as ResponseData
import jwt


class Authentication(authentication.BaseAuthentication):
    """Authenticate user using JWT utility """

    def authenticate(self, request):
        """Function to authenticate token passed in all apis"""
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization').replace("Bearer ", "")
            if not token:
                raise exceptions.AuthenticationFailed('No token provided')
            is_valid, message = JWTUtility.is_token_valid(token)
            if is_valid:
                data = JWTUtility.decode_token(token)
                print("data")
                print(data)
                try:
                    user = UserModel.objects.filter(
                        email=data["email"], mobile_number=data["mobile_number"]).first()
                    if not user:
                        raise exceptions.AuthenticationFailed(
                        'Invalid token')
                except Exception as exc:
                    print(exc)
                    raise exceptions.AuthenticationFailed(
                        'No such user exists')
                return user, None
            if message == "Token is Invalid":
                returndata = {"success": False, "error": message}
                raise exceptions.PermissionDenied(returndata)
            returndata = {"success": False, "error": message}
            raise exceptions.AuthenticationFailed(returndata)
        raise exceptions.AuthenticationFailed('No token provided')
