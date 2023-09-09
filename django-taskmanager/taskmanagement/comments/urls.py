"""Url patterns for comments module"""
from django.urls import path
from . import views

urlpatterns = [
    path('add_new_comment/', views.add_new_comment, name="add_new_comment"),
    path('update_comment/', views.update_comment, name="update_comment"),
    path('delete_comment/', views.delete_comment, name="delete_comment"),
    path('getcomments/', views.getcomments, name="getcomments"),

]
