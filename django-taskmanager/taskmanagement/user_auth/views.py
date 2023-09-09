"""User authentication module"""

import base64
from datetime import datetime
import math
import random
import django
import pyotp
from django.http.response import JsonResponse
from django.contrib.auth import password_validation
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from response import Response as ResponseData
from email_manager import EmailManager
from .serializers import AddUserRoleSerializer, AddUserStatusSerializer, ChangePasswordSerializer, GetAllUsersSerializer, RefreshAuthTokenSerializer
from .serializers import DeleteUserRoleSerializer
from .serializers import DeleteUserStatusSerializer
from .serializers import ForgotPasswordSerializer, GetUserRoleSerializer, GetUserStatusSerializer
from .serializers import ResetPasswordSerializer, SignInSerializer, UpdateUserRoleSerializer
from .serializers import UpdateUserStatusSerializer, UserSerializer, UserUpdateProfileSerializer
from .models import OtpForPasswordModel, UserModel, UserRoleModel, UserStatusModel
from .authentication import Authentication
from django.core.files.storage import FileSystemStorage


# Create your views here.

@swagger_auto_schema(method="POST", request_body=UserSerializer)
@api_view(["POST"])
def signup(request):
    """Function to create new user"""
    try:
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            email_id = serializer.data["email"]
            password = serializer.data["password"]
            role = serializer.data["role"] if serializer.data["role"] != "" else 0
            mobile_number = serializer.data["mobile_number"]
            email = UserModel.objects.filter(email=email_id).first()
            role_data = UserRoleModel.objects.filter(id=role).first()
            profile_pic = request.FILES['profile_pic'] if 'profile_pic' in request.FILES else ""
            if profile_pic!="":
                 fs = FileSystemStorage(location='static/')
                 fs.save(profile_pic.name, profile_pic)
            if not role_data:
                return Response(
                    ResponseData.error("Role id is not valid"),
                    status=status.HTTP_200_OK,
                )
            if UserModel.objects.filter(first_name=first_name).first():
                return Response(
                    ResponseData.error("first name already exists"),
                    status=status.HTTP_200_OK,
                )
            if UserModel.objects.filter(last_name=last_name).first():
                return Response(
                    ResponseData.error("last name already exists"),
                    status=status.HTTP_200_OK,
                )
            if email:
                return Response(
                    ResponseData.error("Email already exists"),
                    status=status.HTTP_200_OK,
                )
            mobile_number_data = UserModel.objects.filter(mobile_number=mobile_number).first()
            if mobile_number_data:
                return Response(
                    ResponseData.error("Mobile Number already exists"),
                    status=status.HTTP_200_OK,
                )
            user_status_data = UserStatusModel.objects.filter(
                user_status="Active"
            ).first()
            user_status_id = ""
            if user_status_data:
                user_status_id = user_status_data.id
            new_user = UserModel.objects.create(
                first_name=first_name,
                profile_pic= "" if profile_pic is "" else f"static/{profile_pic}",
                last_name=last_name,
                email=email_id,
                mobile_number=mobile_number,
                password=password,
                role_id=role,
                status_id=user_status_id,
            )
            new_user.save()
            user_details = list(
                UserModel.objects.values().filter(id=new_user.id))
            user_details[0].pop("is_active")
            user_details[0].pop("is_delete")
            user_details[0].pop("password")
            user_details.append("authentication_token")
            user_details[0]["authentication_token"] = serializer.get_token(
                user_details[0])
            user_details[0]['status_id'] = str(user_details[0]['status_id'])
            user_details[0]['role_id'] = str(user_details[0]['role_id'])
            return Response(
                ResponseData.success(
                    user_details[0], "User created successfully"),
                status=status.HTTP_201_CREATED,
            )
        for error in serializer.errors:
            print(serializer.errors[error][0])
        return Response(
            ResponseData.error(serializer.errors[error][0]),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@swagger_auto_schema(method="POST", request_body=SignInSerializer)
@api_view(["POST"])
def signin(request):
    """Function to let user sign in"""
    try:
        data = request.data
        serializer = SignInSerializer(data=data)
        if serializer.is_valid():
            
            password = serializer.data["password"]
            email = serializer.data["email"]
            user = UserModel.objects.filter(
                email=email, password=password).first()
            if not user:
                return Response(
                    ResponseData.error(
                        "Account does not exists, please register first"),
                    status=status.HTTP_201_CREATED,
                )
            userdata = list(UserModel.objects.values().filter(email=email))
            userdata[0].pop("password")
            userdata[0].pop("is_active")
            userdata[0].pop("is_delete")
            userdata.append("authentication_token")
            userdata[0]["status_id"] = str(userdata[0]["status_id"])
            userdata[0]["authentication_token"] = serializer.get_token(
                userdata[0])
            userdata[0]['role_id'] = str(userdata[0]['role_id'])
            return JsonResponse(
                    ResponseData.success(
                        userdata[0], "User logged in successfully"),
                    safe=False,
                )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(django.utils.timezone.now)) + "Some Random Secret Key"
        

@swagger_auto_schema(method="POST", request_body=ForgotPasswordSerializer)
@api_view(["POST"])
def forgot_password(request):
    """Function to send activation link on email id"""
    try:
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            user_data = UserModel.objects.filter(
                email=email
            ).first()
            if not user_data:
                return Response(ResponseData.success_without_data("Entered email id does not exists"),status=status.HTTP_200_OK)
            digits = "0123456789"
            OTP = ""
            for i in range(6):
               OTP += digits[math.floor(random.random() * 10)]
            otp = list(OTP)
            if otp[0] == "0":
                otp[0] = "1"
                OTP = "" 
                for i in range(0,len(otp)):
                  OTP+=otp[i]
            template = '''
<!DOCTYPE html>
<html>
<body>

<h1>Otp for reseting password</h1>

<p>Your otp is {0}</p>

</body>
</html>
'''.format(OTP)
            EmailManager().forgot_password(
                            email,
                            "Forgot Password",
                            template
                        ),
            user_otp_data = OtpForPasswordModel.objects.filter(
                user_id=user_data.id
            ).first()
            if user_otp_data:
                new_otp_for_forget_password_table = OtpForPasswordModel.objects.update(
                user_id = user_data.id,
                created_at = django.utils.timezone.now,
                otp = OTP
                )
            else:
                new_otp_for_forget_password_table = OtpForPasswordModel.objects.create(
                user_id = user_data.id,
                created_at = django.utils.timezone.now,
                otp = OTP
                )
                new_otp_for_forget_password_table.save()
            return Response(ResponseData.success_without_data("OTP has been sent successfully on your email address"),status=status.HTTP_200_OK)
        return Response(
            ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=ResetPasswordSerializer)
@api_view(["POST"])
def reset_password(request):
    """Function to reset password for the user"""
    try:
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid():
            current_date_time = django.utils.timezone.now
            if serializer.data["password"] != "":
                password_validation.validate_password(
                    serializer.data["password"])
            userotpdata = OtpForPasswordModel.objects.filter(
                otp=data["otp"]).first()
            if not userotpdata:
                return Response(
                    {"success": False, "message": "OTP entered is invalid"},
                    status=status.HTTP_200_OK,
                )
            fmt = '%Y-%m-%d %H:%M:%S'
            current_date = datetime.strptime(str(current_date_time).split(".")[0],fmt)
            otp_generated_date = datetime.strptime(str(userotpdata.created_at).split(".")[0],fmt)
            diff = current_date - otp_generated_date
            if diff.seconds > 60 : 
                OtpForPasswordModel.objects.filter(otp=data["otp"]).delete()
                return Response(
                    {"success": False, "message": "OTP entered is expired"},
                    status=status.HTTP_200_OK,
                )
            print(str(current_date_time).split(".")[0])
            print(str(userotpdata.created_at).split(".")[0])
            userdata = UserModel.objects.filter(
                id=userotpdata.user_id).first()
            userdata.password = serializer.data["password"]
            userdata.save() # Verifying the OTP
            return Response(
                    ResponseData.success_without_data(
                        "Password changed successfully"),
                    status=status.HTTP_200_OK,
                )
        #     else:
        #         return Response(
        #     ResponseData.error("Invalid otp"), status=status.HTTP_400_BAD_REQUEST
        # )
        return Response(
            ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST")
@api_view(["POST"])
def delete_profile(request):
    """Function to delete user profile"""
    try:
        authenticated_user = Authentication().authenticate(request)
        user_id = authenticated_user[0].id
        if not UserModel.objects.filter(id=user_id).first():
                return Response(
                    ResponseData.error("Account does not exists"),
                    status=status.HTTP_201_CREATED,
                )
        UserModel.objects.filter(id=user_id).delete()
        return Response(
                ResponseData.success_without_data(
                    "Profile deleted successfully"),
                status=status.HTTP_200_OK,
            )
        # return Response(
        #     ResponseData.error(serializer.errors),
        #     status=status.HTTP_400_BAD_REQUEST,
        # )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=UserUpdateProfileSerializer)
@api_view(["POST"])
def update_profile(request):
    """Function to update user profile"""
    try:
        authenticated_user = Authentication().authenticate(request)
        print(authenticated_user[0].id)
        data = request.data
        serializer = UserUpdateProfileSerializer(data=data)
        if serializer.is_valid() and authenticated_user:
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            # role = serializer.data["role"] if serializer.data["role"] != "" else 0
            profile_pic = request.FILES['profile_pic'] if 'profile_pic' in request.FILES else ""
            userdata = UserModel.objects.filter(
                id=authenticated_user[0].id
            ).first()
            if not userdata:
                return Response(
                    ResponseData.error("Profile does not exists."),
                    status=status.HTTP_200_OK,
                )
            role = UserRoleModel.objects.filter(
                id=serializer.data["role"]).first()
            if not role:
                return Response(
                    ResponseData.error("Role id is not valid"),
                    status=status.HTTP_200_OK,
                )
            status_id = UserStatusModel.objects.filter(
                id=serializer.data["status"]
            ).first()
            if not status_id:
                return Response(
                    ResponseData.error("Status id is not valid"),
                    status=status.HTTP_200_OK,
                )
            if 'profile_pic' in request.FILES:
                fs = FileSystemStorage(location='static/')
                fs.save(request.FILES['profile_pic'].name, request.FILES['profile_pic'])
            if 'profile_pic' in request.FILES:
               print("profile_pic")
               print(serializer.data["role"])
               userdata.first_name=first_name
               userdata.profile_pic = f"static/{request.FILES['profile_pic']}"
               userdata.last_name=last_name
               userdata.role_id = serializer.data["role"]
               userdata.status_id = status_id
               userdata.save()
               print("true")
            else:
               userdata.first_name=first_name
               userdata.last_name=last_name
               userdata.role_id = serializer.data["role"]
               userdata.status_id = status_id
               userdata.save()
               print("true")
            updated_date = list(
                UserModel.objects.values().filter(
                    id=authenticated_user[0].id)
            )
            updated_date[0].pop("password")
            updated_date[0].pop("is_active")
            updated_date[0].pop("is_delete")
            updated_date[0]['status_id'] = str(updated_date[0]['status_id'])
            updated_date[0]['role_id'] = str(updated_date[0]['role_id'])
            return Response(
                ResponseData.success(
                    updated_date[0], "User profile updated successfully"),
                status=status.HTTP_201_CREATED,
            )
        print("serializer.errors")
        print(serializer.errors)
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except KeyError as exception:
        print("exception")
        print(exception)
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=AddUserStatusSerializer)
@api_view(["POST"])
def add_user_status(request):
    """Function to add user status"""
    try:
        # authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddUserStatusSerializer(data=data)
        if serializer.is_valid():
            
            user_status = serializer.data["user_status"]
            user_status_data = UserStatusModel.objects.filter(
                user_status=user_status,
            ).first()
            if user_status_data:
                return Response(
                    ResponseData.error("This user status already exists"),
                    status=status.HTTP_200_OK,
                )
            new_user_status = UserStatusModel.objects.create(
                user_status=user_status)
            new_user_status.save()
            status_date = list(
                UserStatusModel.objects.values().filter(id=new_user_status.id)
            )
            return Response(
                ResponseData.success(
                    status_date[0], "User Status created successfully"),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=GetUserStatusSerializer)
@api_view(["POST"])
def get_user_status(request):
    """Function to get user status"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetUserStatusSerializer(data=data)
        if serializer.is_valid() and authenticated_user:
            
            user_status_id = serializer.data["id"]
            if user_status_id is None:
                user_status_data = list(UserStatusModel.objects.values())
                if len(user_status_data) == 1:
                    user_status_data[0].pop("is_active")
                    user_status_data[0].pop("is_delete")
                    return Response(
                        ResponseData.success(
                            user_status_data[0], "User status details fetched successfully"),
                        status=status.HTTP_201_CREATED,
                    )
                for i,ele in enumerate(user_status_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                return Response(
                    ResponseData.success(
                        user_status_data, "User status details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
            user_status_data = UserStatusModel.objects.filter(
                id=user_status_id).first()
            if not user_status_data:
                return Response(
                    ResponseData.error(
                        "User status id does not exists or is invalid"),
                    status=status.HTTP_200_OK,
                )
            else:
                user_status_data = list(
                    UserStatusModel.objects.values().filter(id=user_status_id)
                )
                if len(user_status_data) == 0:
                    return Response(
                        ResponseData.success(user_status_data,
                                             "No user status found"),
                        status=status.HTTP_201_CREATED,
                    )
                user_status_data[0].pop("is_active")
                user_status_data[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        user_status_data[0], "User status details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=UpdateUserStatusSerializer)
@api_view(["POST"])
def update_user_status(request):
    """Function to update user status"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = UpdateUserStatusSerializer(data=data)
        if serializer.is_valid():
            
            user_status_id = serializer.data["id"]
            user_status = serializer.data["user_status"]
            if user_status_id != "":
                user_status_data = UserStatusModel.objects.filter(
                    id=user_status_id
                ).first()
                if not user_status_data:
                    return Response(
                        ResponseData.error(
                            "User status id does not exists or is invalid"),
                        status=status.HTTP_200_OK,
                    )
                if user_status_data.user_status == user_status:
                    return Response(
                        ResponseData.error(
                            f"The user status name {user_status} already exists"),
                        status=status.HTTP_200_OK,
                    )
                user_status_data.user_status = user_status
                user_status_data.save()
                user_status_new_data = list(
                    UserStatusModel.objects.values().filter(id=user_status_data.id)
                )
                user_status_new_data[0].pop("is_active")
                user_status_new_data[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        user_status_new_data[0], "User status updated successfully"),
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    ResponseData.error(
                        "Project status id param cannot be empty"),
                    status=status.HTTP_200_OK,
                )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=DeleteUserStatusSerializer)
@api_view(["POST"])
def delete_user_status(request):
    """Function to delete user status"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteUserStatusSerializer(data=data)
        if serializer.is_valid():
            
            user_status_id = serializer.data["id"]
            if not UserStatusModel.objects.filter(id=user_status_id).first():
                return Response(
                    ResponseData.error("User status id does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            UserStatusModel.objects.filter(id=user_status_id).delete()
            return Response(
                ResponseData.success_without_data(
                    "User status deleted successfully"),
                status=status.HTTP_200_OK,
            )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=AddUserRoleSerializer)
@api_view(["POST"])
def add_user_role(request):
    """Function to add user role"""
    try:
        # authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddUserRoleSerializer(data=data)
        if serializer.is_valid():
            user_role = serializer.data["user_role"]
            role_data = UserRoleModel.objects.filter(
                user_role=user_role).first()
            if role_data:
                roles_data = list(
                    UserRoleModel.objects.values().filter(user_role=user_role)
                )
                roles_data[0].pop("is_active")
                roles_data[0].pop("is_delete")
                return Response(
                    ResponseData.error("This user role already exists"),
                    status=status.HTTP_200_OK,
                )
            new_role = UserRoleModel.objects.create(user_role=user_role)
            new_role.save()
            role_data = list(
                UserRoleModel.objects.values().filter(id=new_role.id))
            role_data[0].pop("is_active")
            role_data[0].pop("is_delete")
            return Response(
                ResponseData.success(
                    role_data[0], "User Role created successfully"),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=GetUserRoleSerializer)
@api_view(["POST"])
def get_user_role(request):
    """Function to get user role"""
    try:
        # authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetUserRoleSerializer(data=data)
        if serializer.is_valid():
            
            user_role_id = serializer.data["id"]
            if user_role_id is None:
                user_role_data = list(UserRoleModel.objects.values())
                if len(user_role_data) == 0:
                    return Response(
                        ResponseData.error("No user role found"),
                        status=status.HTTP_201_CREATED,
                    )
                if len(user_role_data) == 1:
                    user_role_data[0].pop("is_active")
                    user_role_data[0].pop("is_delete")
                    return Response(
                        ResponseData.success(
                            user_role_data[0], "User role details fetched successfully"),
                        status=status.HTTP_201_CREATED,
                    )
                for i,ele in enumerate(user_role_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                return Response(
                    ResponseData.success(
                        user_role_data, "User role details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
                
            user_role_data = UserRoleModel.objects.filter(
                id=user_role_id).first()
            if not user_role_data:
                return Response(
                    ResponseData.error(
                        "User role id does not exists or is invalid"),
                    status=status.HTTP_200_OK,
                )
            else:
                user_role_data = list(
                    UserRoleModel.objects.values().filter(id=user_role_id)
                )
                user_role_data[0].pop("is_active")
                user_role_data[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        user_role_data[0], "User role details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=UpdateUserRoleSerializer)
@api_view(["POST"])
def update_user_role(request):
    """Function to update user role"""
    try:
        authenticated_user=Authentication().authenticate(request)
        data = request.data
        serializer = UpdateUserRoleSerializer(data=data)
        if serializer.is_valid():
            
            user_role_id = serializer.data["id"]
            user_role = serializer.data["user_role"]
            if user_role_id != "":
                user_role_data = UserRoleModel.objects.filter(
                    id=user_role_id).first()
                if not user_role_data:
                    return Response(
                        ResponseData.error(
                            "User role id does not exists or is invalid"),
                        status=status.HTTP_200_OK,
                    )
                if user_role_data.user_role == user_role:
                    return Response(
                        ResponseData.error(
                            f"The user role name {user_role} already exists"),
                        status=status.HTTP_200_OK,
                    )
                user_role_data.user_role = user_role
                user_role_data.save()
                user_role_new_data = list(
                    UserRoleModel.objects.values().filter(id=user_role_data.id)
                )
                user_role_new_data[0].pop("is_active")
                user_role_new_data[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        user_role_new_data[0], "User role updated successfully"),
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    ResponseData.error(
                        "Project status id param cannot be empty"),
                    status=status.HTTP_200_OK,
                )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=DeleteUserRoleSerializer)
@api_view(["POST"])
def delete_user_role(request):
    """Function to delete user role"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteUserRoleSerializer(data=data)
        if serializer.is_valid():
            
            user_role_id = serializer.data["id"]
            if not UserRoleModel.objects.filter(id=user_role_id).first():
                return Response(
                    ResponseData.error("User role id does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            UserRoleModel.objects.filter(id=user_role_id).delete()
            return Response(
                ResponseData.success_without_data(
                    "User role deleted successfully"),
                status=status.HTTP_200_OK,
            )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as error:
        return Response(
            ResponseData.error(str(error)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=ChangePasswordSerializer)
@api_view(["POST"])
def change_password(request):
    """Function to changing user password"""
    try:
        authenticated_user = Authentication().authenticate(request)
        print("authenticated_user")
        print(authenticated_user)
        data = request.data
        serializer = ChangePasswordSerializer(data=data)
        if serializer.is_valid() and authenticated_user is not None:
            userdata = UserModel.objects.filter(
                id=authenticated_user[0].id, password=serializer.data["old_password"]
            ).first()
            if not userdata:
                return Response(
                    ResponseData.error("Credentials are incorrect"),
                    status=status.HTTP_200_OK,
                )
            if (
                    serializer.data["new_password"] != ""
                    and serializer.data["old_password"] != ""
            ) and (serializer.data["new_password"] == serializer.data["old_password"]):
                return Response(
                    ResponseData.error("New password is same as previous one"),
                    status=status.HTTP_201_CREATED,
                )
            if serializer.data["new_password"] != "":
                password_validation.validate_password(
                    serializer.data["new_password"])
                userdata.password = serializer.data["new_password"]
                userdata.save()
                return Response(
                    ResponseData.success_without_data(
                        "User password updated successfully"),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                ResponseData.error("Please provide new password value"),
                status=status.HTTP_201_CREATED,
            )
        for error in serializer.errors:
            print(serializer.errors[error][0])
        return Response(
            ResponseData.error(serializer.errors[error][0]),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as error:
        return Response(
            ResponseData.error(str(error)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



@swagger_auto_schema(method="POST")
@api_view(["POST"])
def refresh_token(request):
    """Function to refresh token for a user"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = RefreshAuthTokenSerializer(data=data)
        if authenticated_user is not None:
            print(f"dsvdsdsvs {authenticated_user[0].id}")
            userdata = UserModel.objects.filter(
                id=authenticated_user[0].id
            ).first()
            user_details = list(
                UserModel.objects.values().filter(id=authenticated_user[0].id))
            print(f"dsvdsfs {user_details}")
            user_details[0].pop("is_active")
            user_details[0].pop("is_delete")
            # user_details[0].pop("user_id")
            user_details[0].pop("password")
            user_details[0].pop("first_name")
            user_details[0].pop("last_name")
            user_details[0].pop("status_id")
            user_details[0].pop("profile_pic")
            user_details[0].pop("email")
            user_details[0].pop("mobile_number")
            user_details[0].pop("role_id")
            user_details[0].pop("created_at")
            user_details[0].pop("updated_at")
            user_details[0].pop("id")
            user_details.append("access_token")
            user_details[0]["access_token"] = serializer.get_token(
                userdata)
            return Response(
                ResponseData.success(
                    user_details[0], "Access token generated successfully"),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as error:
        return Response(
            ResponseData.error(str(error)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@swagger_auto_schema(method="POST")
@api_view(["POST"])
def logout(request):
    """Function to logout a user and expire the particular token sent by frontend developer"""
    try:
        authenticated_user = Authentication().authenticate(request)
        # serializer = LogoutUserSerializer(data=data)
        if authenticated_user is not None:
            request.headers.get('Authorization').replace("Bearer ", "").delete()
            return Response(
                ResponseData.success_without_data(
                    "Access token generated successfully"),
                status=status.HTTP_201_CREATED,
            )
        # return Response(
        #     ResponseData.error(serializer.errors),
        #     status=status.HTTP_400_BAD_REQUEST,
        # )
    except Exception as error:
        return Response(
            ResponseData.error(str(error)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@swagger_auto_schema(method='POST', request_body=GetAllUsersSerializer)
@api_view(["POST"])
def get_all_users(request):
    """Function to get all users data"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetAllUsersSerializer(data=data)
        if serializer.is_valid():
            userdata = UserModel.objects.filter(
                id=authenticated_user[0].id
            ).first()
            assigneesdata = list(
                UserModel.objects.values().filter())
            finaldata = []
            if len(assigneesdata) > 0:
                 for i in range(0,len(assigneesdata)):
                     if assigneesdata[i]['id'] != userdata.id:
                         finaldata.append(assigneesdata[i])
            if len(finaldata) == 0:
                return Response(ResponseData.success(
                        finaldata, "No user found"),
                    status=status.HTTP_201_CREATED)
            for i in range(0,len(finaldata)):
                finaldata[i].pop("is_active")
                finaldata[i].pop("is_delete")
                finaldata[i].pop("password")
                finaldata[i]['status_id'] = str(finaldata[i]['status_id'])
            return Response(
                    ResponseData.success(
                        finaldata, "User details details fetched successfully"),
                    status=status.HTTP_201_CREATED)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)