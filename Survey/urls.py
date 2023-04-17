from django.urls import path, re_path
from .views import *

urlpatterns = [ 
	path('api/getSurveys',getSurveys),
	path('api/getSurvey',getSurvey),
	path('api/postSurvey',PostSurvey),
	path('api/saveSurvey',SaveSurvey),
	path('api/sendSurvey',SendSurvey),
	path('api/loadCamera',LoadCamera),
	path('api/saveCameraPictures/',SaveCameraPictures),
	path('api/deleteSurvey', DeleteSurvey),
	path('api/addCategory',AddCategory),	
	path('api/getCategories',GetCategories),
	path('api/addIcon', AddIcon),
	path('api/getProjectIcons', GetProjectIcons),
	path('api/addSelectedIcon',AddSelectedIcon),
	path("api/editIcon", EditIcon),
	path("api/editCategory", EditCategory),
	path("api/deleteCategory", DeleteCategory),
	path("api/deleteIconBase", DeleteIconBase),
	path("api/submitForm", SubmitForm),
	path("api/saveIconInfo", SaveIconInfo),
	path("api/saveNewIcon",SaveNewIcon),
	path("api/changePosition", ChangePosition),
	path("api/iconAttributeChange", IconAttributeChange),
	path("api/deleteIcon",DeleteIcon),
	path("api/handleResolve",HandleResolve),
	path("api/saveNewCable", SaveNewCable),
	path("api/saveLine", SaveLine),
	path("api/changeCable", ChangeCable),
	path("api/handleLock", HandleLock),
	path("api/addLine",AddLine),
	path("api/changeOrder",ChangeOrder),
	path("api/submitLabel", SubmitLabel),
	path("api/convertPDF", convertPDF),
	path("api/delPhoto", DelPhoto),
	path("api/addPhoto", AddPhoto),
	path("api/editSurvToolbar",EditSurvToolbar),
	path("api/editInsToolbar",EditInsToolbar),
	path("api/saveField", SaveField),
	path("api/addComment", AddComment),
	path("api/saveIconSize", SaveIconSize),
    path('api/categoryOrder', CategoryOrder),
    path('api/changeImage', ChangeImage),
    path("api/createSaveSurvey", CreateSaveSurvey),
    path("api/handleOverwrite", HandleOverwrite)
	
]