from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Developer, Skill, Project


class DeveloperInline(admin.StackedInline):
    model = Developer
    can_delete = False
    verbose_name_plural = "developer"


class UserAdmin(BaseUserAdmin):
    inlines = [DeveloperInline]


class SkillAdmin(admin.ModelAdmin):
    model = Skill
    fields = ["level", "language"]


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    fields = [
        "owner",
        "project_name",
        "description",
        "maximum_collaborators",
        "collaborators",
        "status",
        "open_positions",
        "apllied_collaborators",
    ]


admin.site.register(Skill, SkillAdmin)
admin.site.register(Project, ProjectAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
