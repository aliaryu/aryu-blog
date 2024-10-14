from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Profile,
    Follow,
)


class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name = _("profile information")
    classes = ["collapse"]
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return ("deleted_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    inlines = (ProfileInline,)
    ordering = ("-id",)
    search_fields = ("email",)
    # list_display_links = None
    list_display = ("email", "last_name",)
    fieldsets = (
        (_("unique information"), {"fields": ("id", "email",)}),
        (_("personal information"), {"fields": ("first_name", "last_name",)}),
        (_("related dates"), {"fields": ("last_login", "date_joined", "deleted_at",)}),
        (_("access level"), {"fields": ("is_superuser", "is_staff", "is_active", "is_deleted",)}),
        (_("groups & permissions"), {"fields": ("groups", "user_permissions",), "classes": ("collapse",)}),
    )
    readonly_fields = ("id", "last_login", "date_joined", "deleted_at",)
    add_fieldsets = (
        (_("unique information"), {"fields": ("email",)}),
        (_("personal information"), {"fields": ("first_name", "last_name",)}),
        (_("access level"), {"fields": ("is_superuser", "is_staff", "is_active")}),
        (_("password"), {"fields": ("password1", "password2")})
    )
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.archive()
        else:
            return super().get_queryset(request)


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     model = Profile

#     # To save time, complete implementation is omitted.

#     def get_queryset(self, request):
#         if request.user.is_superuser:
#             return self.model.objects.archive().select_related("user")
#         else:
#             return super().get_queryset(request).select_related("user")


admin.site.register([Follow,])
