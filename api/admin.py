from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Society, Tag, Event
from .forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = UserCreationForm

    list_display = ('name', 'email', 'verified')
    list_filter = ('verified',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        (('Info'), {'fields': ('role', 'phone',
                                        'otp', 'otp_expiry', 'verified', 'society', 'fcm_token')}),
        (('Permissions'), {'fields': ('is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {'fields': ('email', 'name', 'password1', 'password2', 'role', 'society')}),
       
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
