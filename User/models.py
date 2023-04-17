from django.db import models
from django.contrib.auth.models import User
from Organization.models import Organization, ClientOrganization

def upload_free_company(instance, filename):
	return "%s%s" %("User/Free_user/",filename)

class Profile(models.Model):
	User = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name="profile")
	first_name= models.CharField(max_length=199, blank=True, null=True)
	last_name= models.CharField(max_length=199, blank=True, null=True)
	email= models.EmailField(max_length=254, blank=True, null=True)
	phone_number= models.CharField(max_length=30, blank=True, null=True)
	company=models.ManyToManyField(Organization)
	clientOrg=models.ForeignKey(ClientOrganization, on_delete=models.SET_NULL, blank=True, null=True, related_name="profile")
	isSuperAdmin=models.BooleanField(default=False, blank=True, null=True)
	isCompanyAdmin=models.BooleanField(default=False, blank=True, null=True)
	isAccountManager=models.BooleanField(default=False, blank=True, null=True)
	isSurveyor=models.BooleanField(default=False, blank=True, null=True)
	isDesigner=models.BooleanField(default=False, blank=True, null=True)
	isProposal=models.BooleanField(default=False, blank=True, null=True)
	isTechnician=models.BooleanField(default=False, blank=True, null=True)
	isClient=models.BooleanField(default=False, blank=True, null=True)
	isFreeUser=models.BooleanField(default=False, blank=True, null=True)
	work_email= models.CharField(max_length=199, blank=True, null=True)
	work_phone_number= models.CharField(max_length=199, blank=True, null=True)
	address= models.CharField(max_length=1999, blank=True, null=True)
	isPrevilageChange=models.BooleanField(default=False, blank=True, null=True)

	def __str__(self):
		return self.first_name+self.last_name

	def fullName(self):
		return self.first_name+self.last_name

class FreeUser(models.Model):
	approved 		=models.BooleanField(default=None, blank=True, null=True)
	username 		=models.CharField(max_length=199, blank=True, null=True)
	first_name 		=models.CharField(max_length=199, blank=True, null=True)
	last_name 		=models.CharField(max_length=199, blank=True, null=True)
	email  			=models.EmailField(max_length=254, blank=True, null=True)
	phone_number 	=models.CharField(max_length=30, blank=True, null=True)
	company_name  	=models.CharField(max_length=399, blank=True, null=True)
	work_number  	=models.CharField(max_length=199, blank=True, null=True)
	work_email  	=models.CharField(max_length=199, blank=True, null=True)
	work_address  	=models.CharField(max_length=1999, blank=True, null=True)
	file 			=models.ImageField(upload_to=upload_free_company, blank=True, null = True)
	date 			=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		name="no name"		
		if self.first_name and self.last_name:
			name=self.first_name+self.last_name
		elif self.username:
			name=self.username
		elif self.email:
			name=self.email		
		return name

	def save(self, *args, **kwargs):
		try:
			this = FreeUser.objects.get(id=self.id)
			if this.file != self.file:
				this.file.delete()
		except: pass
		super(FreeUser, self).save(*args, **kwargs)

