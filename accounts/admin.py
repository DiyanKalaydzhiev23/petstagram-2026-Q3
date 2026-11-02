from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _
from accounts.forms import AppUserCreateForm, AppUserChangeForm

UserModel = get_user_model()

admin.site.unregister(Group)

@admin.register(UserModel)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("usable_password", "password1", "password2"),
            },
        ),
    )
    form = AppUserChangeForm
    add_form = AppUserCreateForm
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

@admin.register(Group)
class GroupUserAdmin(GroupAdmin, ModelAdmin):
    ...
