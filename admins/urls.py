from django.urls import path, include
from admins.views import (home, UserLogin, AdminDashboard, AdminCreateTable, AdminTables, AdminUpdateTable,
AdminOrganizations, AdminCreateOrganization, AdminUpdateOrganization, AdminUserTable, AdminCreateUser,
AdminUserUpdate, AdminSatatusChange, AdminStatistica, AdminSetting, AdminSignOut)

urlpatterns = [
    path('', home, name='home'),
    path('login/', UserLogin.as_view(), name='login'),
    path('sign_out/', AdminSignOut.as_view(), name='sign_out'),
    path('custom_admin/', AdminDashboard.as_view(), name='custom_admin'),
    path('custom_user/', include('users.urls'), name='custom_user'),
    path('custom_admin/requests/', AdminTables.as_view(), name='tables'),
    path('custom_admin/requests/create', AdminCreateTable.as_view(), name='admin_create_table'),
    path('custom_admin/requests/update', AdminUpdateTable.as_view(), name='update_table'),

    path('custom_admin/organizations/', AdminOrganizations.as_view(), name='organizations'),
    path('custom_admin/organizations/create', AdminCreateOrganization.as_view(), name='admin_create_organization'),
    path('custom_admin/organizations/update', AdminUpdateOrganization.as_view(), name='update_organization'),

    path('custom_admin/users/', AdminUserTable.as_view(), name='users'),
    path('custom_admin/users/create', AdminCreateUser.as_view(), name='admin_create_user'),
    path('custom_admin/users/update', AdminUserUpdate.as_view(), name='update_user'),
    
    path('status_change/', AdminSatatusChange.as_view(), name='status_change'),

    path('custom_admin/statistica/', AdminStatistica.as_view(), name='statistica'),
    path('custom_admin/settings', AdminSetting.as_view(), name='settings_admin')
]
