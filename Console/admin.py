from django.contrib import admin
from .models import *

TO_REGISTER=[
	Project, Attachment, Ticket, TicketPicture, ChatFile
]

[admin.site.register(x) for x in TO_REGISTER]