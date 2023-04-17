from django.contrib import admin
from .models import *

TO_REGISTER=[
	Proposal, Section, Page, Element
]

[admin.site.register(x) for x in TO_REGISTER]