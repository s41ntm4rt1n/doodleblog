from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email')}
         ),
    )
admin.site.register(CustomUser, CustomUserAdmin)

class OTPTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code")


admin.site.register(OTPToken, OTPTokenAdmin)