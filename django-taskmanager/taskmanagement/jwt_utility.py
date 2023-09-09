import jwt

from datetime import datetime, timedelta
from django.apps import apps


from taskmanagement import settings


class JWTUtility:
    """
    JWT Utility contains utility methods for dealing with JWTokens using Python JWT

    - JWT_TOKEN_EXPIRY: No. of minutes
    """

    JWT_TOKEN_EXPIRY = getattr(
        settings, "JWT_TOKEN_EXPIRY", timedelta(seconds=10))

    @staticmethod
    def encode_token(User_Model):
        """
        Token created against username of the user.
        """
        print(User_Model)
        if User_Model:
            data = {
                "exp": datetime.utcnow() + timedelta(days=settings.JWT_TOKEN_EXPIRY),
                "email": User_Model["email"],
                "mobile_number": str(User_Model["mobile_number"]),
            }
            config = apps.get_app_config("django_jwt_extended")
            refresh_data = {
                "exp": datetime.utcnow() + config.refresh_token_expires,
                "email": User_Model["email"],
                "mobile_number": str(User_Model["mobile_number"]),
            }
            token = jwt.encode(
                data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
            )
            return {
                "refresh": str(
                    jwt.encode(
                        refresh_data,
                        settings.SECRET_KEY,
                        algorithm=settings.JWT_ALGORITHM,
                    )
                )
                .replace("b'", "")
                .replace("'", ""),
                "access": str(token).replace("b'", "").replace("'", ""),
            }
        # raise User.DoesNotExist


    @staticmethod
    def encode_refresh_token(User_Model):
        """
        Token created against username of the user.
        """
        print(User_Model)
        if User_Model:
            data = {
                "exp": datetime.utcnow() + timedelta(days=settings.JWT_TOKEN_EXPIRY),
                "email": User_Model.email,
                "mobile_number": str(User_Model.mobile_number),
            }
            config = apps.get_app_config("django_jwt_extended")
            refresh_data = {
                "exp": datetime.utcnow() + config.refresh_token_expires,
                "email": User_Model.email,
                "mobile_number": str(User_Model.mobile_number),
            }
            token = jwt.encode(
                data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
            )
            return {
                "refresh": str(
                    jwt.encode(
                        refresh_data,
                        settings.SECRET_KEY,
                        algorithm=settings.JWT_ALGORITHM,
                    )
                )
                .replace("b'", "")
                .replace("'", ""),
                "access": str(token).replace("b'", "").replace("'", ""),
            }
        # raise User.DoesNotExist


    @staticmethod
    def is_token_valid(token):
        """
        Check if token is valid.
        """
        try:
            jwt.decode(token, settings.SECRET_KEY,
                       algorithms=settings.JWT_ALGORITHM)
            return True, "Valid"
        except jwt.ExpiredSignatureError:
            return False, "Token Expired"
        except jwt.InvalidTokenError:
            return False, "Token is Invalid"

    @staticmethod
    def decode_token(token):
        """
        return user for the token given.
        """
        username_dict = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
        print("username_dict")
        print(username_dict)
        return username_dict
