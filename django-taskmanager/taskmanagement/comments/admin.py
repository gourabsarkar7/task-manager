from django.contrib import admin
from comments.models import CommentModel

# Register your models here.
@admin.register(CommentModel)
class CommentsAdmin(admin.ModelAdmin):
    exclude = ("created_at","updated_at","is_active","is_delete")
    pass

