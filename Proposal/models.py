from django.db import models
from Organization.models import Organization
from Survey.models import Survey

def upload_element(instance, filename):
	return "%s%s" %("Proposal/Element/",filename)

def upload_page(instance, filename):
	return "%s%s" %("Proposal/Page/",filename)

def upload_proposal(instance, filename):
	return "%s%s" %("Proposal/Proposal/",filename)

class Proposal(models.Model):
	name= models.CharField(max_length=199, blank=True, null=True)
	typpe= models.CharField(max_length=199, blank=True, null=True)
	proposalid=models.IntegerField(default=1,null=True, blank=True)
	proposCode=models.CharField(default="", max_length=199, blank=True, null=True)
	senderEmail=models.CharField(default="", max_length=199, blank=True, null=True)
	thumbnail=models.FileField(upload_to=upload_proposal, blank=True, null=True)
	survey=models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="proposal", blank=True, null=True)
	company= models.ManyToManyField(Organization)	

	def __str__(self):
		return self.name

	def delete(self, *args, **kwargs):
		self.thumbnail.delete()
		super().delete(*args, **kwargs)

class Section(models.Model):
	no=models.IntegerField(default=1,null=True, blank=True)
	sectionid=models.IntegerField(default=1,null=True, blank=True)
	name= models.CharField(max_length=199, blank=True, null=True)
	proposal=models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="section", blank=True, null=True)

	def __str__(self):
		return self.name

class Page(models.Model):
	no=models.IntegerField(default=1,null=True, blank=True)
	pageid=models.IntegerField(default=1,null=True, blank=True)
	color=models.CharField(max_length=199, blank=True, null=True)
	bgImage=models.FileField(upload_to=upload_page,blank=True, null=True)
	bgUrl=models.CharField(max_length=599, blank=True, null=True)
	proposal=models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="page", blank=True, null=True)
	section=models.ForeignKey(Section, on_delete=models.CASCADE, related_name="page", blank=True, null=True)

	def __str__(self):
		return str(self.pageid)

	def delete(self, *args, **kwargs):
		self.bgImage.delete()
		super().delete(*args, **kwargs)

class Element(models.Model):
	elementid=models.IntegerField(default=1,null=True, blank=True)
	typpe= models.CharField(max_length=199, blank=True, null=True)
	loc=models.CharField(max_length=199, blank=True, null=True)
	configuration=models.CharField(default="", max_length=199, blank=True, null=True)
	image=models.FileField(upload_to=upload_element,blank=True, null=True)
	text=models.TextField(default="", blank=True, null=True)
	imgSize=models.CharField(default="", max_length=199, blank=True, null=True)
	size=models.CharField(default="", max_length=199, blank=True, null=True)
	transform=models.CharField(default="", max_length=199, blank=True, null=True)
	imgUrl=models.CharField(default="", max_length=799, blank=True, null=True)
	section=models.ForeignKey(Section, on_delete=models.CASCADE, related_name="element", blank=True, null=True)
	proposal=models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="element", blank=True, null=True)
	page=models.ForeignKey(Page, on_delete=models.CASCADE, related_name="element", blank=True, null=True)

	def __str__(self):
		return str(self.elementid)

	def delete(self, *args, **kwargs):
		self.image.delete()
		super().delete(*args, **kwargs)