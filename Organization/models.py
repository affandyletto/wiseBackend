from django.db import models

class Organization(models.Model):
	name= models.CharField(max_length=199, blank=True, null=True)
	email= models.EmailField(max_length=254, blank=True, null=True)
	number=models.CharField(max_length=199, blank=True, null=True)
	location=models.CharField(max_length=799, blank=True, null=True)

	def __str__(self):
		return self.name

class ClientOrganization(models.Model):
	name= models.CharField(max_length=199, blank=True, null=True)
	email= models.EmailField(max_length=254, blank=True, null=True)
	number=models.CharField(max_length=20,blank=True, null=True)
	location=models.CharField(max_length=799, blank=True, null=True)
	company=models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="client_org", blank=True, null=True)
	
	def __str__(self):
		return self.name
