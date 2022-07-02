from django.contrib import admin
from core.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'password']

class StaffAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'password']

admin.site.register(User, UserAdmin)