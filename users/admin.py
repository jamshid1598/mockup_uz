from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('User Info', {'fields': ('phonenumber', 'email', 'last_login', 'phone_number_verified', 'change_pw',)}),
        ('User Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('phonenumber', 'email', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'date_joined', 'phone_number_verified', 'change_pw',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('phonenumber', 'email',)
    ordering = ('phonenumber', 'email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)