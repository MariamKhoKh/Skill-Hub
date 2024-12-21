from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Message, Notification


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'date_joined', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'bio', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'bio', 'profile_picture')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Message)
admin.site.register(Notification)