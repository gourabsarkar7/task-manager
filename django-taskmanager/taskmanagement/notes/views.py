"""Apis for note module"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from user_auth.authentication import Authentication
from response import Response as ResponseData
from notes.models import NotesModel
from notes.serializers import AddNoteSerializer
from notes.serializers import DeleteNoteSerializer, GetNoteSerializer
from notes.serializers import UpdateNoteSerializer
from user_auth.models import UserModel


# Create your views here.

@swagger_auto_schema(method='POST', request_body=AddNoteSerializer)
@api_view(["POST"])
def add_new_note(request):
    """Function to add new note"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddNoteSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            # project_id = serializer.data["project_id"]
            # task_id = serializer.data["task_id"]
            title = serializer.data["title"]
            description = serializer.data["description"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(ResponseData.error("User does not exists"),
                                status=status.HTTP_200_OK)
            # if project_id != "":
            #     project = ProjectModel.objects.filter(id=project_id).first()
            #     if not project:
            #         return Response(ResponseData.error("No projects found"),
            #                         status=status.HTTP_200_OK)
            # if task_id != "":
            #     assignee = TaskModel.objects.filter(id=task_id).first()
            #     if not assignee:
            #         return Response(ResponseData.error("No task found"),
            #                         status=status.HTTP_200_OK)
            new_note = NotesModel.objects.create(user_id=user_id, title=title,
                                                 description=description)
            new_note.save()
            notedata = list(NotesModel.objects.values().filter(id=new_note.id))
            notedata[0].pop("is_active")
            notedata[0].pop("is_delete")
            notedata[0]['user_id'] = str(notedata[0]['user_id'])
            return Response(
                ResponseData.success(notedata[0], "Note added successfully"),
                status=status.HTTP_201_CREATED)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=UpdateNoteSerializer)
@api_view(["POST"])
def update_note(request):
    """Function to update note details"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = UpdateNoteSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            note_id = serializer.data["id"]
            # project_id = serializer.data["project_id"]
            # task_id = serializer.data["task_id"]
            title = serializer.data["title"]
            description = serializer.data["description"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(ResponseData.error("User does not exists"),
                                status=status.HTTP_200_OK)
            # if project_id != "":
            #     project_data = ProjectModel.objects.filter(
            #         id=project_id).first()
            #     if not project_data:
            #         return Response(
            #             ResponseData.error(
            #                 "Project id does not exists or is invalid"),
            #             status=status.HTTP_200_OK)
            # if task_id != "":
            #     task_data = TaskModel.objects.filter(id=task_id).first()
            #     if not task_data:
            #         return Response(
            #             ResponseData.error(
            #                 "Task id does not exists or is invalid"),
            #             status=status.HTTP_200_OK)
            notes_data = NotesModel.objects.filter(id=note_id).first()
            if not notes_data:
                return Response(
                    ResponseData.error(
                        "Note id does not exists or is invalid"),
                    status=status.HTTP_200_OK)
            else:
                note = NotesModel.objects.filter(id=note_id).first()
                note.title = title
                note.description = description
                note.save()
                notedata = list(NotesModel.objects.values().filter(id=note.id))
                notedata[0].pop("is_active")
                notedata[0].pop("is_delete")
                notedata[0]['user_id'] = str(notedata[0]['user_id'])
                return Response(
                    ResponseData.success(
                        notedata[0], "Note details updated successfully"),
                    status=status.HTTP_201_CREATED)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=DeleteNoteSerializer)
@api_view(["POST"])
def delete_note(request):
    """Function to delete note"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteNoteSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            note_id = serializer.data["id"]
            # project_id = serializer.data["project_id"]
            # task_id = serializer.data["task_id"]
            note = NotesModel.objects.filter(
                id=note_id).first()
            if not UserModel.objects.filter(id=user_id).first():
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_201_CREATED)
            if not note:
                return Response(
                    ResponseData.success([],"No note found"),
                    status=status.HTTP_201_CREATED)
            NotesModel.objects.filter(
                id=note_id).delete()
            return Response(
                ResponseData.success_without_data("Note deleted successfully"),
                status=status.HTTP_200_OK)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=GetNoteSerializer)
@api_view(["POST"])
def get_note(request):
    """Function to get notes"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetNoteSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            # note_id = serializer.data["id"]
            # project_id = serializer.data["project_id"]
            # task_id = serializer.data["task_id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK)
            # if note_id is None:
            #     notedata = list(NotesModel.objects.values().filter(
            #         user_id=user_id,
            #         project_id=project_id, task_id=task_id))
            #     if not notedata:
            #         return Response(
            #             ResponseData.error("No note found"),
            #             status=status.HTTP_200_OK)
            #     if len(notedata) == 1:
            #         notedata[0].pop("is_active")
            #         notedata[0].pop("is_delete")
            #         return Response(
            #             ResponseData.success(
            #                 notedata[0], "Note details fetched successfully"),
            #             status=status.HTTP_201_CREATED)
            #     for i,ele in enumerate(notedata):
            #         ele.pop("is_active")
            #         ele.pop("is_delete")
            #     return Response(
            #         ResponseData.success(
            #             notedata, "Note details fetched successfully"),
            #         status=status.HTTP_201_CREATED)
            notedata = NotesModel.objects.filter(user_id=user_id).first()
            if not notedata:
                return Response(
                    ResponseData.success([],
                        "No data found"),
                    status=status.HTTP_200_OK)
            else:
                print("called")
                notedata = list(NotesModel.objects.values().filter(
                    user_id=user_id))
                for i in range(0,len(notedata)):
                    notedata[i].pop("is_active")
                    notedata[i].pop("is_delete")
                    notedata[i]['user_id'] = str(notedata[i]['user_id'])
                return Response(
                    ResponseData.success(
                        notedata, "Note details fetched successfully"),
                    status=status.HTTP_201_CREATED)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
