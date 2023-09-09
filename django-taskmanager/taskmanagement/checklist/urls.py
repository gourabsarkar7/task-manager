"""Url patterns for comments module"""
from django.urls import path
from . import views

urlpatterns = [
    path('add_new_checklist/', views.add_new_checklist, name="add_new_checklist"),
    path('update_checklist/', views.update_checklist, name="update_checklist"),
    path('delete_checklist/', views.delete_checklist, name="delete_checklist"),
    path('getchecklist/', views.getchecklist, name="getchecklist"),
]
