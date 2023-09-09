"""Apis for tag module"""
from multiprocessing import AuthenticationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from response import Response as ResponseData
from tags.models import TagModel
from tags.serializers import AddTagSerializer, DeleteTagSerializer
from tags.serializers import GetTagSerializer, UpdateTagSerializer
from tasks.models import TaskModel
from user_auth.authentication import Authentication
from user_auth.models import UserModel


# Create your views here.


@swagger_auto_schema(method="POST", request_body=AddTagSerializer)
@api_view(["POST"])
def addtag(request):
    """Function to add tag"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddTagSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            task_id = serializer.data["task"]
            name = serializer.data["name"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            task = TaskModel.objects.filter(id=task_id).first()
            if not task:
                return Response(
                    ResponseData.error("Task does not exists"),
                    status=status.HTTP_200_OK,
                )
            new_tag = TagModel.objects.create(
                user_id=user_id, task_id=task_id, name=name
            )
            new_tag.save()
            tag_data = list(TagModel.objects.values().filter(id=new_tag.id))
            tag_data[0].pop("is_active")
            tag_data[0].pop("is_delete")
            tag_data[0]['user_id'] = str(tag_data[0]['user_id'])
            tag_data[0]['task_id'] = str(tag_data[0]['task_id'])
            return Response(
                ResponseData.success(tag_data[0], "Tag added successfully"),
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


@swagger_auto_schema(method="POST", request_body=UpdateTagSerializer)
@api_view(["POST"])
def update_tag(request):
    """Function to update tag"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = UpdateTagSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            task_id = serializer.data["task"]
            name = serializer.data["name"]
            tag_id = serializer.data["id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            if task_id != "":
                task_data = TaskModel.objects.filter(id=task_id).first()
                if not task_data:
                    return Response(
                        ResponseData.error("Task id does not exists"),
                        status=status.HTTP_200_OK,
                    )
            tag_data = TagModel.objects.filter(id=tag_id).first()
            if not tag_data:
                return Response(
                    ResponseData.error("Tag id does not exists"),
                    status=status.HTTP_200_OK,
                )
            elif tag_data.name == name:
                return Response(
                    ResponseData.error("Tag name is same as before"),
                    status=status.HTTP_200_OK,
                )
            else:
                tag_data.name = name
                tag_data.save()
                tag = list(TagModel.objects.values().filter(id=tag_data.id))
                tag[0].pop("is_active")
                tag[0].pop("is_delete")
                tag[0]['user_id'] = str(tag[0]['user_id'])
                tag[0]['task_id'] = str(tag[0]['task_id'])
                return Response(
                    ResponseData.success(
                        tag[0], "Tag name updated successfully"),
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


@swagger_auto_schema(method="POST", request_body=DeleteTagSerializer)
@api_view(["POST"])
def delete_tag(request):
    """Function to delete tag"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteTagSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            tag_id = serializer.data["id"]
            tag = TagModel.objects.filter(id=tag_id, user_id=user_id).first()
            if not UserModel.objects.filter(id=user_id).first():
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            if not tag:
                return Response(
                    ResponseData.error("Tag id does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            TagModel.objects.filter(id=tag_id, user_id=user_id).delete()
            return Response(
                ResponseData.success_without_data("Tag deleted successfully"),
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


@swagger_auto_schema(method="POST", request_body=GetTagSerializer)
@api_view(["POST"])
def gettags(request):
    """Function to get tags details"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetTagSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            tag_id = serializer.data["id"]
            if tag_id is None:
                tag_data = list(TagModel.objects.values())
                if len(tag_data) == 0:
                    return Response(
                        ResponseData.success(tag_data, "No tag found"),
                        status=status.HTTP_201_CREATED,
                    )
                if len(tag_data) == 1:
                    tag_data[0].pop("is_active")
                    tag_data[0].pop("is_delete")
                    tag_data[0]['user_id'] = str(tag_data[0]['user_id'])
                    tag_data[0]['task_id'] = str(tag_data[0]['task_id'])
                    return Response(
                        ResponseData.success(
                            tag_data[0], "Tag details fetched successfully"),
                        status=status.HTTP_201_CREATED,
                    )
                for i,ele in enumerate(tag_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                return Response(
                    ResponseData.success(
                        tag_data, "Tag details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
            task_id = serializer.data["task_id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            tag_data = TagModel.objects.filter(
                id=tag_id, task_id=task_id, user_id=user_id
            ).first()
            if not tag_data:
                return Response(
                    ResponseData.error("Tag id does not exists"),
                    status=status.HTTP_200_OK,
                )
            else:
                tags = list(
                    TagModel.objects.values().filter(
                        id=tag_id, task_id=task_id, user_id=user_id
                    )
                )
                tags[0].pop("is_active")
                tags[0].pop("is_delete")
                tags[0]['user_id'] = str(tags[0]['user_id'])
                tags[0]['task_id'] = str(tags[0]['task_id'])
                return Response(
                    ResponseData.success(
                        tags[0], "Tag details fetched successfully"),
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
