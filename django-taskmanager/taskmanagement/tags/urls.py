"""Url patterns for tag module"""
from django.urls import path
from . import views

urlpatterns = [
    path('addtag/', views.addtag, name="addtag"),
    path('update_tag/', views.update_tag, name="update_tag"),
    path('delete_tag/', views.delete_tag, name="delete_tag"),
    path('gettags/', views.gettags, name="gettags"),

]
