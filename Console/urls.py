from django.urls import path
from .views import *

urlpatterns = [
    path('api/loadClient',LoadClient),
    path('api/onSelectOrganization', OnSelectOrganization),
    path('api/registerProject', RegisterProject),
    path('api/editProject', EditProject),
    path('api/editProjectInfo', EditProjectInfo),
    path('api/getProject', GetProject),
    path("api/editStage", EditStage),
    path("api/editAddress", EditAddress),
    path("api/editContact", EditContact),
    path("api/uploadAttachment", UploadAttachment),
    path("api/deleteFile", DeleteFile),
    path("api/editAssigned", EditAssigned),
    path("api/deleteProject", DeleteProject),
    path("api/downloadCsv", DownloadCsv),
    path("api/deleteClient", DeleteClient),    
    path("api/addProjectClient", AddProjectClient),
    path("api/editProjectClient", EditProjectClient),
    path("api/editClientOrg", EditClientOrg),
    path("api/fetchAllData", FetchAllData),
    path("api/fetchAllSurveyData", FetchAllSurveyData),
    path("api/sendNewTicket", SendNewTicket),
    path("api/loadTicketList",LoadTicketList),
    path("api/getTicket",GetTicket),
    path("api/closeTicket",CloseTicket),
    path("api/assignTech", AssignTech),
    path("api/ticketSeen", TicketSeen),
    path("api/submitReply", SubmitReply),
    path("api/liveBuiltsFetch", LiveBuiltsFetch)
]