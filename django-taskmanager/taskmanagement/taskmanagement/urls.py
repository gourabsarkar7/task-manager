"""task management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

Schemaview = get_schema_view(
    openapi.Info(
        title="Task Management API",
        default_version='v1',
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="anirudhflutter@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('task_app/', include("user_auth.urls")),
    path('task_app/', include("projects.urls")),
    path('task_app/', include("tasks.urls")),
    path('task_app/', include("notes.urls")),
    path('task_app/', include("comments.urls")),
    path('task_app/', include("checklist.urls")),
    path('', Schemaview.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('re_doc/', Schemaview.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('json/', Schemaview.without_ui(cache_timeout=0), name='schema-json'),
]

urlpatterns += staticfiles_urlpatterns()