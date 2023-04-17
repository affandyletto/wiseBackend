from django.contrib import admin
from .models import *

TO_REGISTER=[
	Organization, ClientOrganization
]

[admin.site.register(x) for x in TO_REGISTER]