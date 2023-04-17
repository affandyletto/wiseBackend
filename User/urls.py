from django.urls import path
from .views import GetMyInfo,MyTokenObtainPairView, RegisterUser, GetProfiles, ModifyRoles,DeleteUser,EditUser,FreeSubmit,GetFreeUser,FreeApprove

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('api/token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/registerUser',RegisterUser),
    path('api/editUser',EditUser),
    path('api/getProfiles',GetProfiles),
    path('api/modifyRoles', ModifyRoles),
    path("api/deleteUser", DeleteUser),
    path("api/freeSubmit", FreeSubmit),
    path("api/getFreeUser", GetFreeUser),
    path("api/freeApprove", FreeApprove),
    path("api/getMyInfo", GetMyInfo)
]