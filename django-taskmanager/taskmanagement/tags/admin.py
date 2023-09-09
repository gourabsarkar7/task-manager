from django.contrib import admin
from tags.models import TagModel

# Register your models here.
@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    exclude = ("created_at","updated_at","is_active","is_delete")
    pass
