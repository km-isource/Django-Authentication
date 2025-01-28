from django.contrib import admin
from django.utils.text import Truncator
from .models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'truncated_description', 'author', 'created_at')
    
    def truncated_description(self, obj):
        return Truncator(obj.description).chars(100, truncate='.........')
    truncated_description.short_description = 'Description'


