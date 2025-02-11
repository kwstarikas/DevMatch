from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Developer, ProgrammingLanguage


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class DeveloperInline(admin.StackedInline):
    model = Developer
    can_delete = False
    verbose_name_plural = "developer"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [DeveloperInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
