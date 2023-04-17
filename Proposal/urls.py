from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('api/addProposal', AddProposal),
    path('api/addSection', AddSection),
    path('api/addPage', AddPage),
    path('api/addElement', AddElement),
    path('api/fetchProposal',FetchProposal),
    path('api/getProposals', GetProposals),
    path('api/saveThumbnail',SaveThumbnail),
    path("api/editElement", EditElement),
    path("api/sendSign", SendSign),
    path("api/sendSignedProposal", SendSignedProposal),
    path('api/deleteElement', DeleteElement),
    path('api/handleDelete', HandleDelete),
    path('api/changePageBackground', ChangePageBackground)
]