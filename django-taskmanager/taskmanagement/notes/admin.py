from django.contrib import admin
from notes.models import NotesModel

# Register your models here.
@admin.register(NotesModel)
class NotesModel(admin.ModelAdmin):
    exclude = ("created_at","updated_at","is_active","is_delete")
    pass

