from django.contrib import admin
from .models import Role
from .models import User

# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'rol')
    
admin.site.register(Role, RoleAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'email', 'password', 'rol','created_at', 'updated_at')
    
admin.site.register(User, UserAdmin)