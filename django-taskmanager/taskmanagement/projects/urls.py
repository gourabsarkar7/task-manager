"""
Api end points for project module
"""

from django.urls import path
from . import views


urlpatterns = [
    path('addnewproject/', views.add_new_project, name="addnewproject"),
    path('getproject/', views.get_project, name="getproject"),
    path('updateproject/', views.update_project, name="updateproject"),
    path('getallprojects/', views.get_all_projects, name="getallprojects"),
    path('deleteproject/', views.delete_project, name="deleteproject"),
    path('addprojectstatus/', views.add_project_status, name="addprojectstatus"),
    path('getprojectstatus/', views.get_project_status, name="getprojectstatus"),
    path('updateprojectstatus/', views.update_project_status,
         name="updateprojectstatus"),
    path('deleteprojectstatus/', views.delete_project_status,
         name="deleteprojectstatus"),
    path("addprojectassignee/", views.add_project_assignee,
         name="addprojectassignee"),
    path('deleteprojectassignee/', views.delete_project_assignee,
         name="deleteprojectassignee"),
    path('getprojectassignees/', views.get_project_assignees,
         name="getprojectassignees"),
    path('inviteprojectassignees/', views.invite_project_assignees,
         name="inviteprojectassignees"),
    path('index/<int:project_id>/<int:assignee_id>/', views.index, name='myname')
]
