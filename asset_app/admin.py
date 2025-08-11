from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

@admin.action(description="Activate selected users")
def activate_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    messages.success(request, f"Activated {updated} user(s).")

@admin.action(description="Deactivate selected users (skips superusers and yourself)")
def deactivate_users(modeladmin, request, queryset):
    # safety: don't lock yourself out or kill superusers
    safe_qs = queryset.exclude(id=request.user.id).exclude(is_superuser=True)
    skipped = queryset.count() - safe_qs.count()
    updated = safe_qs.update(is_active=False)
    if updated:
        messages.success(request, f"Deactivated {updated} user(s).")
    if skipped:
        messages.warning(request, f"Skipped {skipped} superuser/your own account.")

class CustomUserAdmin(BaseUserAdmin):
    actions = [activate_users, deactivate_users]
    # (optional but nice)
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

# Replace the default User admin
from django.contrib.auth.models import User as DjangoUser
try:
    admin.site.unregister(DjangoUser)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, CustomUserAdmin)
