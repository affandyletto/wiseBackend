from django.db import models
from Organization.models import Organization, ClientOrganization
from User.models import Profile

def upload_audio(instance, filename):
	return "%s%s" %("Ticket/Audio/",filename)

def upload_icon_picture(instance, filename):
	return "%s%s" %("Ticket/picture/",filename)

def upload_chat_file(instance, filename):
	return "%s%s" %("Ticket/chat/",filename)

class Project(models.Model):
	name= models.CharField(max_length=499, blank=True, null=True)	
	number=models.IntegerField(blank=True, null=True)
	company=models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="project")
	clientOrg=models.ManyToManyField(ClientOrganization, related_name="project")
	stage= models.CharField(max_length=199, blank=True, null=True, default="profile")	
	nickname= models.CharField(max_length=199, blank=True, null=True, default="")	
	subCategory= models.CharField(max_length=199, blank=True, null=True)	
	
	#Assigned employee
	client=models.ManyToManyField(Profile, related_name="project")
	accountManager=models.ManyToManyField(Profile,related_name="project_account")
	surveyer=models.ManyToManyField(Profile,related_name="project_surveyer")
	designer=models.ManyToManyField(Profile, related_name="project_designer")
	proposal=models.ManyToManyField(Profile, related_name="project_proposal")
	technician=models.ManyToManyField(Profile, related_name="project_technician")

	#Site contact
	firstName= models.CharField(max_length=299, blank=True, null=True)	
	lastName= models.CharField(max_length=299, blank=True, null=True)	
	email= models.CharField(max_length=299, blank=True, null=True)	
	phone= models.CharField(max_length=199, blank=True, null=True)	

	#date
	startDate=models.DateField(blank=True, null=True)
	endDate=models.DateField(blank=True, null=True)
	hibernate=models.DateField(blank=True, null=True)

	address=models.TextField(blank=True, null=True)
	stageHistory=models.CharField(max_length=3000, blank=True, null=True, default="[]")
	stageStatus=models.CharField(max_length=3000, blank=True, null=True, default="next")

	def __str__(self):
		return self.name

class Attachment(models.Model):
	project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name="attachment")
	file=models.FileField(blank=True, null=True)
	name= models.CharField(max_length=499, blank=True, null=True)	
	def __str__(self):
		return self.project.name

class Ticket(models.Model):
	ticketID= models.CharField(max_length=499, unique=True)
	company=models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="ticket")
	project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name="ticket")
	client=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="ticket")
	technician=models.ManyToManyField(Profile, related_name="ticket_technician")
	clientOrg=models.ForeignKey(ClientOrganization, on_delete=models.SET_NULL, blank=True, null=True, related_name="ticket")

	surveyID=models.CharField(max_length=499,blank=True, null=True, default="")
	dateCreated=models.CharField(max_length=499,blank=True, null=True, default="")
	dateUpdated=models.CharField(max_length=499,blank=True, null=True, default="")

	clientChat= models.TextField(blank=True, null=True, default="[]")
	internalChat= models.TextField(blank=True, null=True, default="[]")

	status= models.CharField(max_length=499,blank=True, null=True)
	subject= models.CharField(max_length=499,blank=True, null=True)
	details= models.TextField(blank=True, null=True, default="")
	code= models.CharField(max_length=99,blank=True, null=True)

	seenByClient=models.BooleanField(default=True)
	seenByAdmin=models.BooleanField(default=True)

	#audio
	audioInfo 	=models.CharField(max_length=800, default="", null=True, blank=True)
	audioFile 	=models.FileField(upload_to=upload_audio, blank=True, null=True)

	def __str__(self):
		return self.ticketID

	def save(self, *args, **kwargs):
		try:
			this = Ticket.objects.get(id=self.id)
			if this.audioFile != self.audioFile:
				this.audioFile.delete()
		except: pass
		super(Ticket, self).save(*args, **kwargs)

class ChatFile(models.Model):
	chatID=models.CharField(default="", max_length=100)
	ticketID= models.CharField(default="", max_length=499)
	file=models.FileField(upload_to=upload_chat_file, blank=True, null = True)

class TicketPicture(models.Model):
	uploader= models.CharField(max_length=20)
	ticket=models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="ticketPicture",null=True, blank=True, default=None)
	picture=models.ImageField(upload_to=upload_icon_picture, blank=True, null = True)

	def __str__(self):
		return str(self.ticket.ticketID)

	def save(self, *args, **kwargs):
		try:
			this = TicketPicture.objects.get(id=self.id)
			if this.picture != self.picture:
				this.picture.delete()
		except: pass
		super(TicketPicture, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.picture.delete(save=False)
		
		super(self.__class__, self).delete(*args, **kwargs)	