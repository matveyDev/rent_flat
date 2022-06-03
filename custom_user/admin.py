from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': (
          'email',
          'password',
          'last_login'
          )}),
        ('Additional Info', {'fields': (
          ('first_name', 'last_name'),
          'phone',
          )}),
        ('Permissions', {'fields': (
          'is_active',
          'is_staff',
          'is_superuser',
          'groups',
          'user_permissions',
          )}),
    )   
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2'),
            'classes': ('wide',)
            }),
    )       
    list_display = ('email', 'is_staff', 'is_superuser', 'last_login')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login',)