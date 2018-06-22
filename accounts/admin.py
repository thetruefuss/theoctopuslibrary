from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'phone_number', 'phone_number_verified', 'member_since')
    date_hierarchy = 'member_since'
admin.site.register(Profile, ProfileAdmin)  # noqa: E305
