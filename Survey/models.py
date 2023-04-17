from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from Console.models import Project, Ticket
from User.models import Profile
import uuid
from django.utils import timezone

def upload_camera_pictures(instance, filename):
	return "%s%s" %("Survey/Picture/CCTV/",filename)

def upload_picture_location(instance, filename):
	return "%s%s" %("Survey/Picture/",filename)

def upload_audio(instance, filename):
	return "%s%s" %("Survey/Audio/",filename)

def upload_file(instance, filename):
	return "%s%s" %("Console/file/",filename)

def upload_temp_location(instance, filename):
	return "%s%s" %("Survey/file/",filename)

def upload_file_survey(instance, filename):
	return "%s%s" %("temp/file/",filename)

def upload_file_pdf(instance, filename):
	return "%s%s" %("temp/pdf/",filename)

def upload_category(instance, filename):
	return "%s%s" %("Icon/file/",filename)
	
def upload_icon_base(instance, filename):
	return "%s%s" %("Icon/file/",filename)

def upload_icon(instance, filename):
	return "%s%s" %("Icon/file/",filename)
	
def upload_icon_picture(instance, filename):
	return "%s%s" %("Icon/picture/",filename)

	
def upload_icon_file(instance, filename):
	return "%s%s" %("Icon/file/",filename)

class Temp(models.Model):
	pdf 			=models.FileField(upload_to=upload_file_pdf, blank=True, null=True)
	picture 		=models.ImageField(upload_to=upload_temp_location, blank=True, null = True)	

class Survey(models.Model):
	name 			=models.CharField(max_length=300, default="", null=True, blank=True)
	version			=models.CharField(max_length=300, default="main")
	uid 			=models.UUIDField(default=uuid.uuid4, editable=True, null=True, blank=True)
	project 		=models.ForeignKey(Project, on_delete=models.CASCADE,related_name="survey", null=True, blank=True)
	date 			=models.DateTimeField(auto_now_add=True)
	distance 		=models.DecimalField(decimal_places=2,default=0, max_digits=12, validators=[MinValueValidator(Decimal(0)), ])
	pixelDistance 	=models.DecimalField(decimal_places=2,default=0, max_digits=12, validators=[MinValueValidator(Decimal(0)), ])
	unit 			=models.CharField(max_length=100, default="", null=True, blank=True)
	picture 		=models.ImageField(upload_to=upload_picture_location, blank=True, null = True)
	surveyPicture 	=models.ImageField(upload_to=upload_picture_location, blank=True, null = True)
	file 			=models.FileField(upload_to=upload_file_survey, blank=True, null=True)	
	degree 			=models.IntegerField(default=0,null=True, blank=True)
	flip 			=models.BooleanField(default=False,null=True, blank=True)
	dateUpdated		=models.DateTimeField(auto_now=True)
	iconSize		=models.IntegerField(default=14,null=True, blank=True)
	stage 			=models.CharField(max_length=100, default="profile", null=True, blank=True)
	stageStatus 	=models.CharField(max_length=100, null=True, blank=True, default="next")

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		try:
			this = Survey.objects.get(id=self.id)
			if this.file != self.file:
				this.file.delete()
			if this.surveyPicture != self.surveyPicture:
				this.surveyPicture.delete()
			if this.picture != self.picture:
				this.picture.delete()
		except: pass

		try:
			# check if there is a related SavedSurvey object
			saved_survey = self.savedSurvey.all()[0]
			saved_survey.dateUpdated = timezone.now()
			saved_survey.save()
		except:
			pass

		super(Survey, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.picture.delete(save=False)
		self.surveyPicture.delete(save=False)
		self.file.delete(save=False)

		super(self.__class__, self).delete(*args, **kwargs)

class SavedSurvey(models.Model):
	name 			=models.CharField(max_length=300, default="", null=True, blank=True)
	mainSurveyID 	=models.CharField(max_length=900, default="", null=True, blank=True)	
	dateCreated		=models.DateTimeField(auto_now_add=True)
	dateUpdated		=models.DateTimeField(auto_now=True)
	survey 			=models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="savedSurvey",null=True, blank=True, default=None)
	project 		=models.ForeignKey(Project, on_delete=models.CASCADE, related_name="savedSurvey",null=True, blank=True, default=None)
	editedProfile  	=models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="savedSurvey", null=True, blank=True, default=None)

	def __str__(self):
		return self.name

class Category(models.Model):
	name      = models.CharField(max_length=300, default="", null=True, blank=True)
	priority = models.IntegerField(default=0, null=True, blank=True)
	thumbnail = models.ImageField(upload_to=upload_category, blank=True, null = True)

	def __str__(self):
		return self.name

	def delete(self, *args, **kwargs):
		self.thumbnail.delete(save=False)
		
		super(self.__class__, self).delete(*args, **kwargs)

class IconBase(models.Model):
	name      = models.CharField(max_length=300, default="", null=True, blank=True)
	category  = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="iconBase")
	thumbnail = models.ImageField(upload_to=upload_icon_base, blank=True, null = True)
	field  	  = models.TextField(blank=True, null=True)
	project   = models.ManyToManyField(Project, related_name="iconBase")

	def __str__(self):
		return self.name

class Icon(models.Model):
	name      	=models.CharField(max_length=300, default="", null=True, blank=True)
	iconid 		=models.CharField(max_length=80,default="",null=True, blank=True)
	order 		=models.IntegerField(default=1, null=True, blank=True)
	survey  	=models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="icon",null=True, blank=True, default=None)
	angle  		=models.IntegerField(default=1,null=True, blank=True)
	depth  		=models.DecimalField(decimal_places=2,default=0, max_digits=6)
	opacity  	=models.IntegerField(default=1,null=True, blank=True)
	color 		=models.CharField(max_length=400, default="", null=True, blank=True)
	bgColor 	=models.CharField(max_length=400, default="#ffff00", null=True, blank=True)
	rotate 		=models.IntegerField(default=45,null=True, blank=True)
	iconRotate 	=models.IntegerField(default=0,null=True, blank=True)
	xposition 	=models.DecimalField(decimal_places=2,default=0, max_digits=12)
	yposition 	=models.DecimalField(decimal_places=2,default=0, max_digits=12)
	unit 		=models.CharField(max_length=800, default="", null=True, blank=True)
	isLocked 	=models.BooleanField(default=False)
	thumbnail 	=models.ImageField(upload_to=upload_icon, blank=True, null = True)
	isReported 	=models.BooleanField(default=False)
	senderReportEmail = models.CharField(default="", null=True, blank=True, max_length=400)

	ticket=models.ManyToManyField(Ticket, related_name="icon")

	#audio
	audioInfo 	=models.CharField(max_length=800, default="", null=True, blank=True)
	audioFile 	=models.FileField(upload_to=upload_audio, blank=True, null=True)
	dateUpdated	=models.DateTimeField(auto_now_add=True)

	#additional info
	startDate		=models.CharField(max_length=100, default="", null=True, blank=True)
	endDate			=models.CharField(max_length=100, default="", null=True, blank=True)
	techName		=models.CharField(max_length=300, default="", null=True, blank=True)
	test            =models.CharField(max_length=1000, default="", null=True, blank=True)
	comment			=models.CharField(max_length=3000, default="", null=True, blank=True)

	surveyToolbar=models.TextField(blank=True, null=True)
	installationToolbar=models.TextField(blank=True, null=True)
	comments=models.TextField(blank=True, null=True)

	iconBase  = models.ForeignKey(IconBase, on_delete=models.SET_NULL, blank=True, null=True, related_name="icon")
	answer 	  = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.iconid)

	def save(self, user=None, *args, **kwargs):
		try:
			this = Icon.objects.get(id=self.id)
			if this.audioFile != self.audioFile:
				this.audioFile.delete()
		except: pass
		
		try:
			saved_survey = self.survey.savedSurvey.all()[0]
			saved_survey.dateUpdated = timezone.now()
			saved_survey.save()	
			if user:
				saved_survey.editedProfile=user.profile
				saved_survey.save()	
		except:
			pass

		super(Icon, self).save(*args, **kwargs)

class Cable(models.Model):
	name      	= models.CharField(max_length=300, default="", null=True, blank=True)
	iconid 		=models.CharField(max_length=80,default="",null=True, blank=True)
	order 		=models.IntegerField(default=1, null=True, blank=True)
	survey  	=models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="cable",null=True, blank=True, default=None)
	iconParent  =models.ForeignKey(Icon, on_delete=models.CASCADE, related_name="cable", null=True, blank=True, default=None)
	depth  		=models.DecimalField(decimal_places=2,default=0, max_digits=6)
	color 		=models.CharField(max_length=400, default="", null=True, blank=True)
	unit 		=models.CharField(max_length=800, default="", null=True, blank=True)
	isLocked 	=models.BooleanField(default=False)
	thumbnail 	= models.ImageField(upload_to=upload_icon, blank=True, null = True)
	line 		= models.TextField(blank=True, null=True, default="")
	label 		= models.TextField(blank=True, null=True)
	answer 	  = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.iconid)

	def save(self, *args, **kwargs):
		try:
			# check if there is a related SavedSurvey object
			saved_survey = self.survey.savedSurvey.all()[0]
			saved_survey.dateUpdated = timezone.now()
			saved_survey.save()
		except:
			pass

		super(Cable, self).save(*args, **kwargs)

class Section(models.Model):
	name      	= models.CharField(max_length=300, default="", null=True, blank=True)
	sectionid 	=models.CharField(max_length=80,default="",null=True, blank=True)
	cableID     =models.IntegerField(default=1,null=True, blank=True)
	order 		=models.IntegerField(default=1, null=True, blank=True)
	cable  		=models.ForeignKey(Cable, on_delete=models.CASCADE, related_name="section",null=True, blank=True, default=None)
	depth  		=models.DecimalField(decimal_places=2,default=0, max_digits=6)
	color 		=models.CharField(max_length=400, default="", null=True, blank=True)
	unit 		=models.CharField(max_length=800, default="", null=True, blank=True)
	isReported 	=models.BooleanField(default=False)
	senderReportEmail = models.CharField(default="", null=True, blank=True, max_length=400)
	x1 			=models.DecimalField(decimal_places=2,default=0, max_digits=6)
	x2 			=models.DecimalField(decimal_places=2,default=0, max_digits=6)
	y1 			=models.DecimalField(decimal_places=2,default=0, max_digits=6)
	y2 			=models.DecimalField(decimal_places=2,default=0, max_digits=6)
	pathType 	=models.CharField(max_length=500, default="", null=True, blank=True)
	note 		=models.TextField(blank=True, null=True)
	#audio
	audioInfo 	=models.CharField(max_length=800, default="", null=True, blank=True)
	audioFile 	=models.FileField(upload_to=upload_audio, blank=True, null=True)
	dateUpdated	=models.DateTimeField(auto_now_add=True)

	#additional info
	startDate		=models.CharField(max_length=100, default="", null=True, blank=True)
	endDate			=models.CharField(max_length=100, default="", null=True, blank=True)
	techName		=models.CharField(max_length=300, default="", null=True, blank=True)
	test            =models.CharField(max_length=1000, default="", null=True, blank=True)
	comment			=models.CharField(max_length=3000, default="", null=True, blank=True)

	answer 	  = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.sectionid)

	def save(self, *args, **kwargs):
		try:
			this = Section.objects.get(id=self.id)
			if this.audioFile != self.audioFile:
				this.audioFile.delete()
		except: pass

		try:
			# check if there is a related SavedSurvey object
			saved_survey = self.survey.savedSurvey.all()[0]
			saved_survey.dateUpdated = timezone.now()
			saved_survey.save()
		except:
			pass

		super(Section, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.audioFile.delete(save=False)
		
		super(self.__class__, self).delete(*args, **kwargs)

class IconFile(models.Model):
	icon=models.ForeignKey(Icon, on_delete=models.CASCADE, related_name="iconFile",null=True, blank=True, default=None)
	section=models.ForeignKey(Section, on_delete=models.CASCADE, related_name="sectionFile",null=True, blank=True, default=None)
	file=models.FileField(upload_to=upload_icon_file, blank=True, null = True)

	def __str__(self):
		return str(self.icon.iconid)

	def save(self, *args, **kwargs):
		try:
			this = IconFile.objects.get(id=self.id)
			if this.file != self.file:
				this.file.delete()
		except: pass
		super(IconPicture, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.file.delete(save=False)
		
		super(self.__class__, self).delete(*args, **kwargs)	

class IconPicture(models.Model):
	icon=models.ForeignKey(Icon, on_delete=models.CASCADE, related_name="iconPicture",null=True, blank=True, default=None)
	section=models.ForeignKey(Section, on_delete=models.CASCADE, related_name="sectionPicture",null=True, blank=True, default=None)
	picture=models.ImageField(upload_to=upload_icon_picture, blank=True, null = True)

	def __str__(self):
		return str(self.icon.iconid)

	def save(self, *args, **kwargs):
		try:
			this = IconPicture.objects.get(id=self.id)
			if this.picture != self.picture:
				this.picture.delete()
		except: pass
		super(IconPicture, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.picture.delete(save=False)
		
		super(self.__class__, self).delete(*args, **kwargs)	