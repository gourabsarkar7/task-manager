from typing import Optional, Sequence
from django.contrib import admin
from projects.models import ProjectModel,ProjectStatusModel

# Register your models here.
@admin.register(ProjectModel)
class ProjectModelAdmin(admin.ModelAdmin):
    exclude = ("created_at","updated_at","is_active","is_delete")
    pass

# Register your models here.
@admin.register(ProjectStatusModel)
class ProjectStatusModelAdmin(admin.ModelAdmin):
    exclude = ("created_at","updated_at","is_active","is_delete")
    pass