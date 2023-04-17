from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('api/registerCompany',RegisterCompany),
    path('api/getCompanies',GetCompanies),
    path('api/editCompany',EditCompany),
    path('api/editClientOrganization',EditClientOrganization),
    path('api/getClientOrganizations',GetClientOrganizations),
    path('api/registerClientOrg',RegisterClientOrg),
    path('api/loadClientOrg',LoadClientOrg),
    path('api/getAvailProfiles', GetAvailProfiles),
    path("api/assignClientUser", AssignClientUser)
]