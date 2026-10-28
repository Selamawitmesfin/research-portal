from django.contrib import admin

from .models import Project, Resource


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "resource_type", "country", "year", "uploaded_at")
    search_fields = ("title", "description")
    list_filter = ("resource_type", "country", "year")
    filter_horizontal = ("projects",)
