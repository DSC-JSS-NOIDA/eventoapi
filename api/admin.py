from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('name', 'email', 'verified')
    list_filter = ('verified',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        (('Personal info'), {'fields': ('role', 'phone', 'otp', 'otp_expiry', 'verified', 'status')}),
        (('Permissions'), {'fields': ('is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )




admin.site.register(User, CustomUserAdmin)
