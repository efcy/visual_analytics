from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import VATUser, Organization


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("organization",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("organization",)}),)

    # Optionally, display organization in the list view
    list_display = UserAdmin.list_display + ("organization",)


admin.site.register(VATUser, CustomUserAdmin)
admin.site.register(Organization)
