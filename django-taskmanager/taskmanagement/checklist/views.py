"""Comment module"""
from multiprocessing.dummy import Array
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from checklist.models import ChecklistDetailModel
from user_auth.models import UserModel
from user_auth.authentication import Authentication
from response import Response as ResponseData
from checklist.models import ChecklistModel
from checklist.serializers import AddChecklistSerializer
from checklist.serializers import DeleteChecklistSerializer
from checklist.serializers import GetChecklistSerializer, UpdateChecklistSerializer
from django.forms.models import model_to_dict
# Create your views here.


@swagger_auto_schema(method="POST", request_body=AddChecklistSerializer,)
@api_view(["POST"])
def add_new_checklist(request):
    """Function to add new checklist"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddChecklistSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            title = serializer.initial_data['title']
            color = serializer.initial_data['color']
            options_for_checklist = serializer.initial_data["options"]
            user = UserModel.objects.filter(id=user_id,email = authenticated_user[0].email,
            mobile_number = authenticated_user[0].mobile_number).first()
            checklistdata = ChecklistModel.objects.filter(title=title).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            if checklistdata:
                return Response(
                    ResponseData.error("Title already exists"),
                    status=status.HTTP_200_OK,
                )
            new_checklist = ChecklistModel.objects.create(
                user_id=user_id,
                title=title,
                color=color
            )
            new_checklist.save()
            print(options_for_checklist)
            for i in range(0,len(options_for_checklist)):
                new_checklist_details = ChecklistDetailModel.objects.create(
                    user_id=user_id,
                    checklist_id=new_checklist.id,
                    checklist_detail=options_for_checklist[i],
                )
                new_checklist_details.save()
            print("alled")
            checklist = list(
                ChecklistModel.objects.values().filter(id=new_checklist.id),
                )
            checklistdetails = list(
                ChecklistDetailModel.objects.values().filter(checklist_id = new_checklist.id),
                )
            checklist[0]["options_details"] = checklistdetails
            checklist[0].pop("is_active")
            checklist[0].pop("is_delete")
            checklist[0].pop("created_at")
            checklist[0].pop("updated_at")
            checklist[0]['user_id'] = str(checklist[0]['user_id'])
            for i in range(0,len(checklist[0]["options_details"])):
                checklist[0]["options_details"][i].pop("created_at")
                checklist[0]["options_details"][i].pop("updated_at")
                checklist[0]["options_details"][i].pop("is_active")
                checklist[0]["options_details"][i].pop("is_delete")
                checklist[0]["options_details"][i]['user_id'] = str(checklist[0]["options_details"][i]['user_id'])
                checklist[0]["options_details"][i]['checklist_id'] = str(checklist[0]["options_details"][i]['checklist_id'])
            return Response(
                ResponseData.success(
                    checklist[0], "Checklist added successfully"),
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


@swagger_auto_schema(method="POST", request_body=UpdateChecklistSerializer)
@api_view(["POST"])
def update_checklist(request):
    """Function to update an existing checklist"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = UpdateChecklistSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            checklist_option_id = serializer.initial_data["id"]
            is_completed = serializer.initial_data["is_completed"]
            title = serializer.data["title"] if serializer.data["title"] is not None else ""
            color = serializer.data["color"] if serializer.data["color"] is not None else ""
            checklist_details = ChecklistDetailModel.objects.filter(id=checklist_option_id).first()
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            checklistcopy = ChecklistModel.objects.filter(id=checklist_details.checklist_id).first()
            if not checklistcopy:
                return Response(
                    ResponseData.error("Checklist does not exists"),
                    status=status.HTTP_200_OK,
                )
            elif not checklist_details:
                return Response(
                    ResponseData.error("Checklist details does not exists"),
                    status=status.HTTP_200_OK,
                )
            else:
                if title != "":
                   checklistcopy.title = title
                if color != "":
                   checklistcopy.color = color
                checklistcopy.save()
                if is_completed == "true" or  is_completed == "True": 
                    is_completed = True
                else:
                    is_completed = False
                checklist_details.is_completed =  is_completed
                checklist_details.save()
                checklist = list(
                ChecklistModel.objects.values().filter(user_id = user_id,id=checklistcopy.id),
                )
                checklistdetails = list(
                ChecklistDetailModel.objects.values().filter(checklist_id = checklistcopy.id,user_id = user_id),
                )
                checklist[0]["options_details"] = checklistdetails
                checklist[0].pop("is_active")
                checklist[0].pop("is_delete")
                checklist[0].pop("created_at")
                checklist[0].pop("updated_at")
                checklist[0]['user_id'] = str(checklist[0]['user_id'])
                for i in range(0,len(checklist[0]["options_details"])):
                    checklist[0]["options_details"][i].pop("created_at")
                    checklist[0]["options_details"][i].pop("updated_at")
                    checklist[0]["options_details"][i].pop("is_active")
                    checklist[0]["options_details"][i].pop("is_delete")
                    checklist[0]["options_details"][i]['user_id'] = str(checklist[0]["options_details"][i]['user_id'])
                    checklist[0]["options_details"][i]['checklist_id'] = str(checklist[0]["options_details"][i]['checklist_id'])
                return Response(
                    ResponseData.success(
                        checklist, "Checklist details updated successfully"),
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


@swagger_auto_schema(method="POST", request_body=DeleteChecklistSerializer)
@api_view(["POST"])
def delete_checklist(request):
    """Function to delete comment"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteChecklistSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            checklist_id = serializer.initial_data["id"]
            checklist = ChecklistModel.objects.filter(
                id=checklist_id,
            ).first()
            if not UserModel.objects.filter(id=user_id).first():
                return Response(
                    ResponseData.error("Account does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            if not checklist:
                return Response(
                    ResponseData.error("Checklist does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            ChecklistModel.objects.filter(
                id=checklist_id,
            ).delete()
            checklistdetails = list(
                ChecklistDetailModel.objects.values().filter(checklist_id=checklist_id),
                )
            for i in range(0,len(checklistdetails)):
                ChecklistDetailModel.objects.filter(
                id=checklistdetails[i].id,
            ).delete()
            return Response(
                ResponseData.success_without_data(
                    "Checklist deleted successfully"),
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


@swagger_auto_schema(method="POST", request_body=GetChecklistSerializer)
@api_view(["POST"])
def getchecklist(request):
    """Function to get checklist"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetChecklistSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            checklist_id = serializer.data["id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            if checklist_id is None:
                checklist = list(
                ChecklistModel.objects.values().filter(user_id = user_id),
                )
                checklistdetails = list(
                ChecklistDetailModel.objects.values().filter(user_id = user_id),
                )
                for i in range(0,len(checklist)):
                    checklist[i]["options_details"] = []
                for i in range(0,len(checklist)):
                    for j in range(0,len(checklistdetails)):
                        if checklist[i]["id"] == checklistdetails[j]["checklist_id"]:
                            checklist[i]["options_details"].append(checklistdetails[j])
                if not checklist:
                    return Response(
                        ResponseData.error("No checklist found"),
                        status=status.HTTP_200_OK,
                    )
                if len(checklist) == 1:
                    checklist[0]["options_details"] = checklistdetails
                    checklist[0].pop("is_active")
                    checklist[0].pop("is_delete")
                    checklist[0].pop("created_at")
                    checklist[0].pop("updated_at")
                    checklist[0]['user_id'] = str(checklist[0]['user_id'])
                    for i in range(0,len(checklist[0]["options_details"])):
                        checklist[0]["options_details"][i].pop("created_at")
                        checklist[0]["options_details"][i].pop("updated_at")
                        checklist[0]["options_details"][i].pop("is_active")
                        checklist[0]["options_details"][i].pop("is_delete")
                        checklist[0]["options_details"][i]['user_id'] = str(checklist[0]["options_details"][i]['user_id'])
                        checklist[0]["options_details"][i]['checklist_id'] = str(checklist[0]["options_details"][i]['checklist_id'])
                    return Response(
                        ResponseData.success(
                            checklist, "Checklist details fetched successfully"),
                        status=status.HTTP_201_CREATED,
                    )
                for i in range(0,len(checklist)):
                    # checklist[i]["options_details"] = checklistdetails
                    checklist[i].pop("is_active")
                    checklist[i].pop("is_delete")
                    checklist[i].pop("created_at")
                    checklist[i].pop("updated_at")
                    print("called")
                    checklist[i]['user_id'] = str(checklist[0]['user_id'])
                    print(checklist[i]["options_details"])
                    for j in range(0,len(checklist[i]["options_details"])):
                        checklist[i]["options_details"][j].pop("created_at")
                        checklist[i]["options_details"][j].pop("updated_at")
                        checklist[i]["options_details"][j].pop("is_active")
                        checklist[i]["options_details"][j].pop("is_delete")
                        checklist[i]["options_details"][j]['user_id'] = str(checklist[i]["options_details"][j]['user_id'])
                        checklist[i]["options_details"][j]['checklist_id'] = str(checklist[i]["options_details"][j]['checklist_id'])
                print(user_id)                                   
                return Response(
                    ResponseData.success(
                        checklist, "Checklist details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
            checklist = list(
                ChecklistModel.objects.values().filter(id=checklist_id,user_id = user_id),
                )
            if len(checklist) == 0:
                return Response(
                    ResponseData.error(
                        "Checklist does not exists or id is invalid"),
                    status=status.HTTP_200_OK,
                )
            else:
                checklistdetails = list(
                ChecklistDetailModel.objects.values().filter(checklist_id = checklist[0]["id"],user_id = user_id),
                )
                checklist[0]["options_details"] = checklistdetails
                checklist[0].pop("is_active")
                checklist[0].pop("is_delete")
                checklist[0].pop("created_at")
                checklist[0].pop("updated_at")
                checklist[0]['user_id'] = str(checklist[0]['user_id'])
                for i in range(0,len(checklist[0]["options_details"])):
                    checklist[0]["options_details"][i].pop("created_at")
                    checklist[0]["options_details"][i].pop("updated_at")
                    checklist[0]["options_details"][i].pop("is_active")
                    checklist[0]["options_details"][i].pop("is_delete")
                    checklist[0]["options_details"][i]['user_id'] = str(checklist[0]["options_details"][i]['user_id'])
                    checklist[0]["options_details"][i]['checklist_id'] = str(checklist[0]["options_details"][i]['checklist_id'])
                return Response(
                    ResponseData.success(
                        checklist, "Checklist details fetched successfully"),
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
