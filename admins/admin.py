from django.contrib import admin
from admins.models import User, Organization, Table

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'password', 'role')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'organization', 'created_at')
    search_fields = ('user__name', 'organization__title')
    fields = ('user', 'organization', 'status')
    
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return self.readonly_fields
    #     return []
