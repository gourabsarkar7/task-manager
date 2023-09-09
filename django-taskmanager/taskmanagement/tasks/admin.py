from django.contrib import admin
from tasks.models import TaskPriorityModel
from tasks.models import TaskModel,TaskStatusModel

# Register your models here.
@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    exclude = ("created_at","updated_at","is_active","is_delete")
    pass

@admin.register(TaskStatusModel)
class TaskStatusAdmin(admin.ModelAdmin):
    exclude = ("created_at","updated_at","is_active","is_delete")
    pass

@admin.register(TaskPriorityModel)
class TaskPriorityAdmin(admin.ModelAdmin):
    exclude = ("created_at","updated_at","is_active","is_delete")
    pass
