from django.urls import path
from users.views import UserDashboard, UserRequest, UserRequestCreate, UserChangeStatus, UserRequestUpdate, UserOrganizations, UserOrganizationsCreate

urlpatterns = [
    path('', UserDashboard.as_view(), name='custom_user'),
    path('requests/', UserRequest.as_view(), name='user_requests'),
    path('requests/create/', UserRequestCreate.as_view(), name='user_request_create'),
    path('user_status_change/', UserChangeStatus.as_view(), name='user_status_change'),
    path('requests/update/', UserRequestUpdate.as_view(), name='user_request_update'),
    path('organizations/', UserOrganizations.as_view(), name='user_organizations'),
    path('organizations/create/', UserOrganizationsCreate.as_view(), name='user_organizations_create'),
]