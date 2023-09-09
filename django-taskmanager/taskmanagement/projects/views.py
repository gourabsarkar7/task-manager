"""Apis for project module"""
from multiprocessing import AuthenticationError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.template import loader
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from email_manager import EmailManager
from user_auth.authentication import Authentication
from user_auth.models import UserModel
from response import Response as ResponseData
from projects.serializers import AddProjectAssigneeSerializer
from projects.serializers import AddProjectSerializer
from projects.serializers import AddProjectStatusSerializer
from projects.serializers import DeleteProjectAssigneeSerializer
from projects.serializers import DeleteProjectSerializer
from projects.serializers import DeleteProjectStatusSerializer
from projects.serializers import GetProjectAssigneeSerializer
from projects.serializers import GetProjectSerializer
from projects.serializers import GetProjectStatusSerializer
from projects.serializers import InviteProjectAssigneeSerializer
from projects.serializers import UpdateProjectSerializer
from projects.serializers import UpdateProjectStatusSerializer
from .models import ProjectAssigneeModel, ProjectModel, ProjectStatusModel


# Create your views here.


@api_view(["GET"])
def index(request,project_id, assignee_id):
    """Function to add assignee into project after verification & display message via html link"""
    project_assignees = ProjectAssigneeModel.objects.create(
        project_id=project_id, assignee_ids=assignee_id
    )
    project_assignees.save()
    template = loader.get_template("content.html")  # getting our template
    return HttpResponse(template.render())


@swagger_auto_schema(method="POST", request_body=AddProjectSerializer)
@api_view(["POST"])
def add_new_project(request):
    """Function to add new project"""
    authenticated_user = Authentication().authenticate(request)
    try:
        data = request.data
        serializer = AddProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            name = serializer.data["name"]
            color = serializer.data["color"]
            description = serializer.data["description"]
            is_private = serializer.data["is_private"]
            duration = serializer.data["duration"]
            archive = serializer.data["archive"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            status_data = ProjectStatusModel.objects.filter(
                project_status="Pending"
            ).first()
            status_id = ""
            if status_data:
                status_id = status_data.id
            project_data = ProjectModel.objects.filter(
                user_id=user_id, name=name
            ).first()
            if project_data:
                return Response(
                    ResponseData.error(
                        "Project with same name already exists"),
                    status=status.HTTP_200_OK,
                )
            new_project = ProjectModel.objects.create(
                user_id=user_id,
                name=name,
                color=color,
                status_id=status_id,
                description=description,
                is_private=is_private,
                archive=archive,
                duration=duration,
            )
            new_project.save()
            project_data = list(
                ProjectModel.objects.values().filter(id=new_project.id))
            project_data[0].pop("is_active")
            project_data[0].pop("is_delete")
            project_data[0]['user_id'] = str(project_data[0]['user_id'])
            project_data[0]['status_id'] = str(project_data[0]['status_id'])
            return Response(
                ResponseData.success(
                    project_data[0], "Project added successfully"),
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


@swagger_auto_schema(method="POST", request_body=GetProjectSerializer)
@api_view(["POST"])
def get_project(request):
    """Function to get project details"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            project_id = serializer.data["id"]
            if project_id is None:
                project_data = list(
                    ProjectModel.objects.values().filter(user_id=user_id)
                )
                if not project_data:
                    return Response(
                        ResponseData.success([],"No projects found"),
                        status=status.HTTP_200_OK,
                    )
                if len(project_data) == 1:
                    project_data[0].pop("is_active")
                    project_data[0].pop("is_delete")
                    project_data[0]['user_id'] = str(project_data[0]['user_id'])
                    project_data[0]['status_id'] = str(project_data[0]['status_id'])
                    return Response(
                        ResponseData.success(
                            project_data[0], "Project details fetched successfully"),
                        status=status.HTTP_201_CREATED,
                    )
                for i,ele in enumerate(project_data):
                    project_data[i]['user_id'] = str(project_data[i]['user_id'])
                    project_data[i]['status_id'] = str(project_data[i]['status_id'])
                    ele.pop("is_active")
                    ele.pop("is_delete")
                return Response(
                    ResponseData.success(
                        project_data, "Project details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            project_data = ProjectModel.objects.filter(id=project_id).first()
            if not project_data:
                return Response(
                    ResponseData.error(
                        "Project id does not exists or is invalid"),
                    status=status.HTTP_200_OK,
                )
            project_data = list(
                ProjectModel.objects.values().filter(id=project_id))
            project_data[0].pop("is_active")
            project_data[0].pop("is_delete")
            project_data[0]['user_id'] = str(project_data[0]['user_id'])
            project_data[0]['status_id'] = str(project_data[0]['status_id'])
            return Response(
                ResponseData.success(
                    project_data[0], "Project details fetched successfully"),
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


@swagger_auto_schema(method="POST", request_body=UpdateProjectSerializer)
@api_view(["POST"])
def update_project(request):
    """Function to update project details"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = UpdateProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            project_id = serializer.data["id"]
            name = serializer.data["name"]
            color = serializer.data["color"]
            project_status_id = (
                serializer.data["status"]
                if serializer.data["status"] != ""
                else ""
            )
            description = serializer.data["description"]
            is_private = serializer.data["is_private"]
            duration = serializer.data["duration"]
            archive = serializer.data["archive"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            project_data = ProjectModel.objects.filter(id=project_id).first()
            if not project_data:
                return Response(
                    ResponseData.error(
                        "Project id does not exists or is invalid"),
                    status=status.HTTP_200_OK,
                )
            if serializer.data["status"] != "":
                project_status_data = ProjectStatusModel.objects.filter(
                    id=project_status_id
                ).first()
                if not project_status_data:
                    return Response(
                        ResponseData.error(
                            "Project status id does not exists"),
                        status=status.HTTP_200_OK,
                    )
            project = ProjectModel.objects.filter(id=project_id).first()
            project.name = name
            project.color = color
            project.status_id = project_status_id
            project.description = description
            project.is_private = is_private
            project.archive = archive
            project.duration = duration
            project.save()
            print("updated")
            project_data = list(
                ProjectModel.objects.values().filter(id=project.id))
            project_data[0].pop("is_active")
            project_data[0].pop("is_delete")
            project_data[0]['user_id'] = str(project_data[0]['user_id'])
            project_data[0]['status_id'] = str(project_data[0]['status_id'])
            return Response(
                ResponseData.success(
                    project_data[0], "Project details updated successfully"),
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


@swagger_auto_schema(method="POST", request_body=GetProjectSerializer)
@api_view(["POST"])
def get_all_projects(request):
    """Function to get all project details"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            project_data = list(
                ProjectModel.objects.values().filter(user_id=user_id))
            if not project_data:
                return Response(
                    ResponseData.success([],"No projects found"),
                    status=status.HTTP_200_OK,
                )
            for i,ele in enumerate(project_data):
                ele.pop("is_active")
                ele.pop("is_delete")
                project_data[i]['user_id'] = str(project_data[i]['user_id'])
                project_data[i]['status_id'] = str(project_data[i]['status_id'])
            return Response(
                ResponseData.success(
                    project_data, "Project details fetched successfully"),
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


@swagger_auto_schema(method="POST", request_body=DeleteProjectSerializer)
@api_view(["POST"])
def delete_project(request):
    """Function to delete project"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            project_id = serializer.data["id"]
            if not UserModel.objects.filter(id=user_id).first():
                return Response(
                    ResponseData.error("Account does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            if not ProjectModel.objects.filter(id=project_id).first():
                return Response(
                    ResponseData.error("Project does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            ProjectModel.objects.filter(id=project_id).delete()
            return Response(
                ResponseData.success_without_data(
                    "Project deleted successfully"),
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


@swagger_auto_schema(method="POST", request_body=AddProjectStatusSerializer)
@api_view(["POST"])
def add_project_status(request):
    """Function to add project status"""
    try:
        # authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddProjectStatusSerializer(data=data)
        if serializer.is_valid():
            
            project_status = serializer.data["project_status"]
            status_data = ProjectStatusModel.objects.filter(
                project_status=project_status
            ).first()
            if status_data:
                return Response(
                    ResponseData.error("Project status already exists"),
                    status=status.HTTP_200_OK,
                )
            new_project_status = ProjectStatusModel.objects.create(
                project_status=project_status
            )
            new_project_status.save()
            project_status_data = list(
                ProjectStatusModel.objects.values().filter(id=new_project_status.id)
            )
            project_status_data[0].pop("is_active")
            project_status_data[0].pop("is_delete")
            return Response(
                ResponseData.success(
                    project_status_data[0], "Project status added successfully"),
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


@swagger_auto_schema(method="POST", request_body=GetProjectStatusSerializer)
@api_view(["POST"])
def get_project_status(request):
    """Function to get project status"""
    try:
        # authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetProjectStatusSerializer(data=data)
        if serializer.is_valid():
            
            project_status_id = serializer.data["id"]
            if project_status_id is None:
                project_status_data = list(ProjectStatusModel.objects.values())
                if not project_status_data:
                    return Response(
                        ResponseData.success([],"No project status found"),
                        status=status.HTTP_200_OK,
                    )
                if len(project_status_data) == 1:
                    project_status_data[0].pop("is_active")
                    project_status_data[0].pop("is_delete")
                    return Response(
                        ResponseData.success(
                            project_status_data[0], "Project status details fetched successfully"),
                        status=status.HTTP_201_CREATED,
                    )
                for i,ele in enumerate(project_status_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                return Response(
                    ResponseData.success(
                        project_status_data, "Project status details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
            project_status_data = ProjectStatusModel.objects.filter(
                id=project_status_id
            ).first()
            if not project_status_data:
                return Response(
                    ResponseData.error(
                        "Project status id does not exists or is invalid"),
                    status=status.HTTP_200_OK,
                )
            else:
                project_status_data = list(
                    ProjectStatusModel.objects.values().filter(id=project_status_id)
                )
                project_status_data[0].pop("is_active")
                project_status_data[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        project_status_data[0], "Project status details fetched successfully"),
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


@swagger_auto_schema(method="POST", request_body=UpdateProjectStatusSerializer)
@api_view(["POST"])
def update_project_status(request):
    """Function to update project status"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = UpdateProjectStatusSerializer(data=data)
        if serializer.is_valid():
            
            project_status_id = serializer.data["id"]
            project_status = serializer.data["project_status"]
            if project_status_id != "":
                project_status_data = ProjectStatusModel.objects.filter(
                    id=project_status_id
                ).first()
                if not project_status_data:
                    return Response(
                        ResponseData.error(
                            "Project status id does not exists or is invalid"),
                        status=status.HTTP_200_OK,
                    )
                if project_status_data.project_status == project_status:
                    return Response(
                        ResponseData.error(
                            f"The project name {project_status} already exists"),
                        status=status.HTTP_200_OK,
                    )
                project_status_data.project_status = project_status
                project_status_data.save()
                project_status_data = list(
                    ProjectStatusModel.objects.values().filter(id=project_status_data.id)
                )
                project_status_data[0].pop("is_active")
                project_status_data[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        project_status_data[0], "Project status updated successfully"),
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


@swagger_auto_schema(method="POST", request_body=DeleteProjectStatusSerializer)
@api_view(["POST"])
def delete_project_status(request):
    """Function to delete project status"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteProjectStatusSerializer(data=data)
        if serializer.is_valid():
            
            project_status_id = serializer.data["id"]
            if not ProjectStatusModel.objects.filter(id=project_status_id).first():
                return Response(
                    ResponseData.error(
                        "Project status id does not exists or is invalid"),
                    status=status.HTTP_201_CREATED,
                )
            ProjectStatusModel.objects.filter(id=project_status_id).delete()
            return Response(
                ResponseData.success_without_data(
                    "Project status deleted successfully"),
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


@api_view(["GET"])
def add_project_assignee(request):
    """Function to add project assignee"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddProjectAssigneeSerializer(data=data)
        if serializer.is_valid():
            
            project_id = serializer.data["project"]
            assignee_ids = serializer.data["assignee_ids"]
            assignee_ids = str(assignee_ids).split(",")
            project_data = ProjectModel.objects.filter(id=project_id).first()
            if not project_data:
                return Response(
                    ResponseData.success([],"Project does not exists"),
                    status=status.HTTP_200_OK,
                )
            if len(assignee_ids) != 0:
                for i,ele in enumerate(assignee_ids):
                    user = UserModel.objects.filter(
                        id=int(ele)).first()
                    if not user:
                        return Response(
                            ResponseData.error(
                                f"Assignee with {ele} does not exists"),
                            status=status.HTTP_200_OK,
                        )

            for i,ele in enumerate(assignee_ids):
                existing_project_assignee_data = list(
                    ProjectAssigneeModel.objects.values().filter(
                        project_id=project_id, assignee_ids=ele
                    )
                )
                if existing_project_assignee_data:
                    return Response(
                        ResponseData.error(
                            f"Assignee with {ele} already exists in this project"),
                        status=status.HTTP_200_OK,
                    )
                project_assignees = ProjectAssigneeModel.objects.create(
                    project_id=project_id, assignee_ids=ele
                )
                project_assignees.save()
            project_assignees_data = list(
                ProjectAssigneeModel.objects.values().filter(
                    project_id=project_assignees.project_id
                )
            )
            project_assignees_data[0].pop("is_active")
            project_assignees_data[0].pop("is_delete")
            project_assignees_data[0]['project_id'] = str(project_assignees_data[0]['project_id'])
            project_assignees_data[0]['user_id'] = str(project_assignees_data[0]['user_id'])
            return Response(
                ResponseData.success(project_assignees_data,
                                     "Project assignees added successfully"),
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


@swagger_auto_schema(method="POST", request_body=DeleteProjectAssigneeSerializer)
@api_view(["POST"])
def delete_project_assignee(request):
    """Function to delete project assignee"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteProjectAssigneeSerializer(data=data)
        if serializer.is_valid():
            
            project_id = serializer.data["project"]
            assignee_ids = serializer.data["assignee_ids"]
            assignee_ids = str(assignee_ids).split(",")
            project_data = ProjectModel.objects.filter(id=project_id).first()
            if not project_data:
                return Response(
                    ResponseData.success([],"Project does not exists"),
                    status=status.HTTP_200_OK,
                )
            if len(assignee_ids) != 0:
                for i,ele in enumerate(assignee_ids):
                    user = UserModel.objects.filter(
                        id=int(ele)).first()
                    if not user:
                        return Response(
                            ResponseData.error(
                                f"Assignee with {ele} does not exists in this project"),
                            status=status.HTTP_200_OK,
                        )
                    ProjectAssigneeModel.objects.filter(
                        assignee_ids=ele
                    ).delete()

            return Response(
                ResponseData.success_without_data(
                    "assignees deleted successfully"),
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


@swagger_auto_schema(method="POST", request_body=GetProjectAssigneeSerializer)
@api_view(["POST"])
def get_project_assignees(request):
    """Function to get project assignee"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetProjectAssigneeSerializer(data=data)
        if serializer.is_valid():
            
            project_id = serializer.data["project"]
            project_data = list(
                ProjectModel.objects.values().filter(id=project_id))
            if not project_data:
                return Response(
                    ResponseData.success([],"Project does not exists"),
                    status=status.HTTP_200_OK,
                )
            project_assignee_data = list(
                ProjectAssigneeModel.objects.values().filter(project_id=project_id)
            )
            if len(project_assignee_data) == 0:
                return Response(
                    ResponseData.success([], "No project assignee found"),
                    status=status.HTTP_201_CREATED,
                )
            for i,ele in enumerate(project_assignee_data):
                ele.pop("is_active")
                ele.pop("is_delete")
                ele.pop("user_id")
                project_assignee_data[i]['project_id'] = str(project_assignee_data[i]['project_id'])
                project_assignee_data[i]['user_id'] = str(project_assignee_data[i]['user_id'])
            return Response(
                ResponseData.success(
                    project_assignee_data, "Project assignee details fetched successfully"),
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


@swagger_auto_schema(method="POST", request_body=InviteProjectAssigneeSerializer)
@api_view(["POST"])
def invite_project_assignees(request):
    """Function to invite project assignee"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = InviteProjectAssigneeSerializer(data=data)
        if serializer.is_valid():
            project_id = serializer.data["project"]
            assignee_ids = serializer.data["assignee_ids"]
            assignee_ids = str(assignee_ids).split(",")
            user_id = authenticated_user[0].id
            project_data = ProjectModel.objects.filter(
                id=project_id, user_id=user_id
            ).first()
            userdata = UserModel.objects.filter(id=user_id).first()
            if not userdata:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_200_OK,
                )
            if not project_data:
                return Response(
                    ResponseData.success([],"Project does not exists"),
                    status=status.HTTP_200_OK,
                )
            if len(assignee_ids) != 0:
                for i,ele in enumerate(assignee_ids):
                    if user_id == ele:
                        return Response(
                            ResponseData.error(
                                "User id and assignee id cannot be same"),
                            status=status.HTTP_200_OK,
                        )
                    user = UserModel.objects.filter(
                        id=int(ele)).first()
                    if not user:
                        return Response(
                            ResponseData.error(
                                f"Assignee with {ele} does not exists"),
                            status=status.HTTP_200_OK,
                        )
            for i,ele in enumerate(assignee_ids):
                existing_project_assignee_data = ProjectAssigneeModel.objects.values().filter(
                    project_id=project_id, assignee_ids=ele
                )
                if existing_project_assignee_data:
                    return Response(
                        ResponseData.error(
                            f"Assignee with {ele} already exists in this project"),
                        status=status.HTTP_200_OK,
                    )
                assignee_data = UserModel.objects.filter(
                    id=ele).first()
                if assignee_data:
                    print(project_id)
                    print(assignee_data.id)
                    template = '''
<!DOCTYPE html>
<html>
<body>

<h1>Verification to assign project</h1>

<p>Click on verify button to get access of the project you have been assigned</p>

<form action="http://127.0.0.1:8000/task_app/index/{0}/{1}/" method="post">

    <input type="submit" value="Verify" />
</form>
<p id="demo"></p>
</body>
</html>
'''.format(project_id,assignee_data.id)
                    return Response(
                        EmailManager().send_email(
                            assignee_data.email,
                            "Get project access",
                            int(project_id),
                            int(assignee_data.id),
                            template
                        ),
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
