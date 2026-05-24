from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'views_count']
    list_display_links = ['id', 'title']
    readonly_fields = ['id', 'created_at', 'views_count']
