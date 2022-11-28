from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User, SignupToken


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "full_name",
                    "avatar",
                    "bio",
                    "location",
                    "socials",
                    "last_login",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "password1", "password2"),
            },
        ),
    )

    list_display = ("email", "full_name", "username", "last_login")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = (
        "email",
        "full_name",
    )
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, UserAdmin)
admin.site.register(SignupToken, admin.ModelAdmin)
