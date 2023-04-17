import os 
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid
from Survey.models import SavedSurvey
from random import randint

def DuplicateImage(name, picture):
	#Duplicating old survey background
	image_name, image_extension = os.path.splitext(name)
	new_image_name = image_name + '_copy' + image_extension
	new_image_file = SimpleUploadedFile(new_image_name, picture.read(), content_type='image/jpeg')
	return new_image_file

def DuplicateSurvey(x, stage, stageStatus, profile, version):
	icons=x.icon.all().prefetch_related('iconPicture')
	newPic=DuplicateImage(x.picture.name,x.picture)
	x.pk=None
	x.picture=newPic
	x.uid=uuid.uuid4()
	x.stage=stage
	x.stageStatus=stageStatus
	x.version=version
	x.save()	
	naraname=x.name+"offline"
	SavedSurvey.objects.create(name=naraname, mainSurveyID=x.name, survey=x, editedProfile=profile, project=x.project)
	for y in icons:
		iconPictures=y.iconPicture.all()
		y.pk=None
		randomId=randint(10000000000000, 99999999999999)
		y.iconid=str(randomId)
		y.project=x
		y.save()
		for z in iconPictures:
			z.pk=None
			z.icon=y
			z.save()

	return x.id