from django.contrib import admin
from .models import *
# Register your models here.
TO_REGISTER=[
	Profile, FreeUser
]

[admin.site.register(x) for x in TO_REGISTER]