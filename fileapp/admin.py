from django.contrib import admin
from .models import User, File  # Make sure these models exist in models.py

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'last_login', 'last_logout')
    search_fields = ('username', 'email')
    list_filter = ('is_admin',)

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'owner', 'upload_time')
    search_fields = ('filename', 'owner__username')
    list_filter = ('upload_time',)
