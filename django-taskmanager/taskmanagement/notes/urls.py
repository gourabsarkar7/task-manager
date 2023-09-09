"""Url patterns for note module"""
from django.urls import path
from . import views

urlpatterns = [
    path('add_new_note/', views.add_new_note, name="add_new_note"),
    path('update_note/', views.update_note, name="update_note"),
    path('delete_note/', views.delete_note, name="delete_note"),
    path('get_note/', views.get_note, name="get_note"),
]
