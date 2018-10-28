from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Society, Tag, Event


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('name', 'email', 'verified')
    list_filter = ('verified',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        (('Info'), {'fields': ('role', 'phone',
                                        'otp', 'otp_expiry', 'verified', 'society')}),
        (('Permissions'), {'fields': ('is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        (('Personal info'), {'fields': ('role', 'phone',
                                        'otp', 'otp_expiry', 'verified')}),
    )



class EventAdmin(admin.ModelAdmin):
    exclude = ('creater',)
    def save_model(self, request, obj, form, change):
        obj.creater = request.user
        obj.save()



admin.site.register(User, CustomUserAdmin)
admin.site.register(Society)
admin.site.register(Tag)
admin.site.register(Event, EventAdmin)
