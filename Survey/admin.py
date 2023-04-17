from django.contrib import admin
from .models import *

TO_REGISTER=[
	Survey,Category, IconBase, Icon, IconPicture, Temp, Cable, Section, SavedSurvey
]

[admin.site.register(x) for x in TO_REGISTER]
