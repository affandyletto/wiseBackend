from django.shortcuts import render
from .serializers import *
from .models import Survey,Category,IconBase, Icon, IconPicture, Temp, Cable, Section, SavedSurvey
from rest_framework.response import Response
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_403_FORBIDDEN,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK,
	HTTP_401_UNAUTHORIZED
)
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from django.core.mail import EmailMessage
import json
import io
from Console.models import Project
from Console.helper import DuplicateImage
import base64
from django.core.files.base import ContentFile
import ast
import fitz
from PIL import Image 
import os 
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import uuid
from random import randint
from django.core.files.uploadedfile import SimpleUploadedFile

@api_view(['POST'])
def convertPDF(request):
	pdf=request.data['pdf']
	for x in Temp.objects.all():
		x.pdf.delete()
		x.picture.delete()
		x.delete()
	temp=Temp.objects.create(pdf=pdf)
	filename = os.path.join(settings.MEDIA_ROOT ,temp.pdf.name)
	doc=fitz.open(filename)
	#doc = open(str(request.get_host())+survey.file.url)
	for page in doc:
		pix = page.get_pixmap()
		output = os.path.join(settings.MEDIA_ROOT, "temp.png")
		pix.save(output)
	mediaURL="temp.png"

	temp.picture=mediaURL
	temp.save()
	darata={
		'url':temp.picture.url
	}
	return Response(temp.picture.url, status=HTTP_200_OK)

@api_view(['POST'])
def PostSurvey(request):

	picture=request.data['selectedFile']
	pixelDistance = request.data.get('pixelDistance')
	distance = request.data.get('distance')
	unit = request.data.get('unit')	
	degree=request.data.get("degree")
	flip=request.data.get('flip')
	name=request.data.get("name")
	projectID=request.data.get("id")
	project=Project.objects.get(id=projectID)
	stage=project.stage
	stageStatus="next"
	flip=True if flip=="true" else False

	surv=Survey.objects.create(
	project=project,
	 picture=picture,
	 pixelDistance=pixelDistance,
	 distance=distance,
	 unit=unit,
	 flip=flip,
	 name=name,
	 stage=project.stage,
	 stageStatus="next",
	 degree=degree)

	naraname=name+"V1"
	SavedSurvey.objects.create(name=naraname, mainSurveyID=name, survey=surv, editedProfile=request.user.profile, project=surv.project)

	return Response(status=204)

@api_view(['POST'])
def ChangeOrder(request):
	data=json.loads(request.data['icons'])
	for x in data:
		icon=Icon.objects.get(iconid=x['id'])
		icon.order=x['order']
		icon.save(user=request.user)
	return Response(status=204)

@api_view(['POST'])
def SaveSurvey(request):
	icon=request.data['cctv']
	survey_id=request.data['surveyID']
	survey=Survey.objects.get(id=survey_id)
	for x in icon:
		try:			
			icon=Icon.objects.get(iconid=x['id'])
			icon.name=x['name']
			icon.order=x['order'] 
			icon.angle=x['angle'] 			
			icon.depth=x['depth'] 
			icon.opacity=x['trans'] 
			icon.color=x['color'] 
			icon.rotate=x['direction']
			icon.xposition=x['xposition'] 
			icon.yposition=x['yposition']
			icon.isLocked=x['isLocked']
			icon.unit=x['unit']		
			icon.answer=str(x['info']['fields'])
			icon.save(user=request.user)
		except:
			iconBase=IconBase.objects.get(id=x['iconBaseID'])
			thumbnail=iconBase.thumbnail
			icon=Icon.objects.create(iconid=x['id'],
				name=x['name'],
				order=x['order'], 
				survey=survey,
				angle=x['angle'], 			
				depth=x['depth'], 
				opacity=x['trans'], 
				color=x['color'], 
				rotate=x['direction'], 
				xposition=x['xposition'], 
				yposition=x['yposition'],
				isLocked=x['isLocked'],
				unit=x['unit'],			
				iconBase=iconBase,	
				thumbnail=thumbnail,
				answer=str(x['info']['fields'])
				)

	serializer=SurveySerializer(survey, many=False)
	return Response(serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def SaveIconInfo(request):
	res=request.data
	for k,v in res.items():
		if k=="type":
			typpe=v
		elif k=="mainInfo":
			if typpe=="section":
				ress=json.loads(v)
			else:
				ress=False
		elif k=="selectedElement":
			try:
				testt=v["addInfo"]["test"]
				startDate=v['addInfo']['startDate']
				endDate=v['addInfo']['endDate']
				comment=v["addInfo"]["comment"]
				techName=v["addInfo"]["techName"]
			except:
				testt=""
				startDate=""
				endDate=""
				comment=""
				techName=""

			v=json.loads(v)
			if typpe=="icon":
				element=Icon.objects.get(iconid=v["id"])
				elementPictures=IconPicture.objects.filter(icon=element)
			elif typpe=="section":
				element=Section.objects.get(sectionid=v["id"])
				elementPictures=IconPicture.objects.filter(section=element)	
			for x in elementPictures:
				x.delete()

			if ress:
				element.label=ress['label']
				element.pathType=ress['pathType']
				element.note=ress['note']
				cable=element.cable
				cable.label=ress['label']
				cable.save()

			element.answer=v['info']['fields']
			element.startDate=startDate
			element.endDate=endDate
			element.test=testt
			element.comment=comment
			element.techName=techName
			element.save()			
		elif "pictures" in k:
			if typpe=="icon":
				IconPicture.objects.create(icon=element, picture=v)
			else:
				IconPicture.objects.create(section=element, picture=v)
		elif k=="audio":
			if v!="null":
				element.audioInfo=v
				element.save()
		elif k=="audioBlob":
			element.audioFile.delete()
			element.save()
			element.audioFile=v
			element.save()

	return Response("SUCCESS", status=HTTP_200_OK)

@api_view(['POST'])
def SaveCameraPictures(request):
	res=request.data
	for k,v in res.items():
		if k=="surveyID":
			survey=Survey.objects.get(id=int(v))
		elif k=="survey_iconSize":
			survey.iconSize=v
			survey.save()
		elif k=="survey_image":
			survey.surveyPicture=v
			survey.save()
			picPath = os.path.join(settings.MEDIA_ROOT ,survey.surveyPicture.name)
			image = Image.open(picPath) 
			img = image.convert('RGB')
			img.save(os.path.join(settings.MEDIA_ROOT ,str(survey.id)+survey.name+".pdf"), format="PDF")
			survey.file=os.path.join(settings.MEDIA_ROOT ,str(survey.id)+survey.name+".pdf")
			survey.save()
	return Response("SUCCESS", status=HTTP_200_OK)

@api_view(['POST'])
def SendSurvey(request):
	email=request.data['email']
	survey_id=request.data['survey_id']
	subject=request.data['subject']
	address=request.data['project_address']	
	survey=Survey.objects.get(id=survey_id)

	if survey.project.address:
		addresss=json.loads(survey.project.address)
		addr=addresss['address']+", "+addresss['city']+", "+addresss['state']+", "+addresss['zipcode']
	else:
		addr="None"	

	email = EmailMessage(str(subject), "Project Address : \n"+addr, to=[email])             
	email.content_subtype = "html" 
	try:
		email.attach(survey.name, survey.surveyPicture.read(), "image/JPEG")
		email.send()
		return Response("success", status=HTTP_200_OK)
	except:
		return Response("Please save the floorplan first", status=HTTP_200_OK)

	return Response("success", status=HTTP_200_OK)
	

@api_view(['POST'])
def LoadCamera(request):
	req=request.data
	survey=Survey.objects.get(id=req)
	icons=Icon.objects.filter(survey=survey)
	cables=Cable.objects.filter(survey=survey).prefetch_related("section")
	newArrayCables=[]
	newArraySections=[]
	if settings.MAIN:
		url="https://main.wiseeyes.link"
	else:
		url="http://127.0.0.1:8000"
	for x in cables:	
		sections=Section.objects.filter(cableID=x.iconid)
		for y in sections:
			pic_list=[]

			for q in y.sectionPicture.all():			
				pic_url=url+request.build_absolute_uri(q.picture.url)
				pic_list.append(pic_url)

			if y.audioInfo:
				audio_info=json.loads(y.audioInfo)
				audio_dummy={
					'blobURL':url+request.build_absolute_uri(y.audioFile.url),
					'startTime':audio_info['startTime'],
					'stopTime':audio_info['stopTime'],
					'options':audio_info['options']
				}
			else:
				audio_dummy=None
			if y.answer:
				arrayInfo = ast.literal_eval(y.answer)
			else:
				arrayInfo=[]
			dummySection={
				"id":y.sectionid,
				"name":y.name,
				"depth":y.depth,
				"unit":y.unit,
				"order":y.order,
				"cableID":x.iconid,
				"isReported":y.isReported,
				"label":x.label,
				"pathType":y.pathType,
				"note":y.note,
				"x1":y.x1,
				"x2":y.x2,
				"y1":y.y1,
				"y2":y.y2,
				"senderReportEmail":y.senderReportEmail,
				'info':{
					'fields':arrayInfo,
					'pictures':pic_list,
					'audio':audio_dummy
				},
				'addInfo':{
					'startDate':y.startDate,
					'endDate':y.endDate,
					'techName':y.techName,
					'test':y.test,
					'comment':y.comment,
				}
			}
			newArraySections.append(dummySection)

		if x.answer:
			arrayInfo = ast.literal_eval(x.answer)
		else:
			arrayInfo=[]

		dummy={
			'id':x.iconid,
			'name':x.name,
			'color':x.color,
			'depth':x.depth,
			'unit':x.unit,
			'isLocked':x.isLocked,	
			'label':x.label,
			'order':x.order,
			"field":arrayInfo
		}
		newArrayCables.append(dummy)

	newArrayIcons=[]
	for x in icons:
		pic_list=[]
		file_list=[]
		for y in x.iconPicture.all():			
			pic_url=request.build_absolute_uri(y.picture.url)
			pic_list.append(pic_url)
		for y in x.iconFile.all():
			file_url=request.build_absolute_uri(y.file.url)
			file_list.append(file_url)

		if x.audioInfo:
			audio_info=json.loads(x.audioInfo)
			audio_dummy={
				'blobURL':request.build_absolute_uri(x.audioFile.url),
				'startTime':audio_info['startTime'],
				'stopTime':audio_info['stopTime'],
				'options':audio_info['options']
			}
		else:
			audio_dummy=None
		arrayInfo = ast.literal_eval(x.answer)
		iconBBase=""
		if x.iconBase:
			iconBBase=x.iconBase.id

		ticketsID=''
		if x.ticket.all():			
			ticketsID=x.ticket.all()[0].ticketID

		dummy={
			'id':x.iconid,
			'name':x.name,
			'order':x.order,
			'xposition':x.xposition,
			'yposition':x.yposition,
			'direction':x.rotate,
			'trans':x.opacity,
			'color':x.color,
			'bgColor':x.bgColor,
			'iconRotate':x.iconRotate,
			'angle':x.angle,
			'depth':x.depth,
			'unit':x.unit,
			'isLocked':x.isLocked,
			'image':url+x.thumbnail.url,
			'iconBaseID':iconBBase,
			'dateUpdated':x.dateUpdated,
			'isReported':x.isReported,			
			'info':{
				'fields':arrayInfo,
				'pictures':pic_list,
				'audio':audio_dummy
			},
			'addInfo':{
				'startDate':x.startDate,
				'endDate':x.endDate,
				'techName':x.techName,
				'test':x.test,
				'comment':x.comment,
			},		
			'surveyToolbar':x.surveyToolbar,
			'installationToolbar':x.installationToolbar,
			'comments':x.comments,
			'ticketID':ticketsID,
			"fileList":file_list
		}
		newArrayIcons.append(dummy)
	res={
		"icons":newArrayIcons,
		"cables":newArrayCables,
		"lines":newArraySections
	}

	return Response(res, status=HTTP_200_OK)

@api_view(['POST'])
def ChangeCable(request):
	cableReq=json.loads(request.data['cable'])
	cable=Cable.objects.get(iconid=cableReq['id'])
	cable.color=cableReq['color']
	cable.label=cableReq['label']
	cable.save()
	return Response("Success", status=HTTP_200_OK)

@api_view(['GET'])
def getSurveys(request):
	serializer=SurveySerializer(Survey.objects.all(), many=True)
	return Response(serializer.data, status=HTTP_200_OK)

@api_view(['POST'])
def getSurvey(request):
	from Console.serializers import ProjectDetailSerializer

	survey_id=request.data.get('id')
	survey=Survey.objects.select_related('project').get(id=survey_id)
	savedSurvey=SavedSurvey.objects.filter(mainSurveyID=str(survey.name), project__id=survey.project.id)
	proj=survey.project
	icons=IconBase.objects.filter(project=proj)
	project=Project.objects.get(id=proj.id)
	projectSerializer=ProjectDetailSerializer(project, many=False)

	categories=Category.objects.all()
	categorySerializer=CategorySerializer(categories, many=True)
	savedSurveySerializer=SavedSurveySerializer(savedSurvey, many=True)
	serializer=SurveySerializer(survey, many=False)
	iconSerializer=IconBaseSerializer(icons, many=True)
	res={
		"survey":serializer.data,
		"savedSurvey":savedSurveySerializer.data,
		"icons":iconSerializer.data,
		"project":projectSerializer.data,
		'categories':categorySerializer.data
	}
	return Response(res, status=HTTP_200_OK)

@api_view(['POST'])
def DeleteSurvey(request):
	survey_id=request.data
	sarurvey=Survey.objects.get(id=survey_id)
	if sarurvey.version == 'main':
		saraved=SavedSurvey.objects.filter(mainSurveyID=sarurvey.savedSurvey.all()[0].mainSurveyID)		
		sarurvey.delete()
		surrv=saraved[0].survey
		surrv.version='main'
		surrv.save()
	return Response("Deleted", status=HTTP_200_OK)

@api_view(['GET'])
def GetCategories(request):
	categories=Category.objects.all()
	serializer=CategorySerializer(categories, many=True)
	icons=IconBase.objects.filter(category__isnull=True)
	serializerIcon=IconBaseSerializer(icons, many=True)
	res={
		"categories":serializer.data,
		"unsortedIcons":serializerIcon.data
	}
	return Response(res, status=HTTP_200_OK)

@api_view(['POST'])
def AddCategory(request):	
	name=request.data['name']
	category=Category.objects.create(name=name)
	try:
		icons=request.data['icons']
		for x in icons:
			icon=IconBase.objects.get(id=x['id'])
			icon.category=category
			icon.save()
	except:
		pass
	
	return Response(status=HTTP_200_OK)

@api_view(['POST'])
def AddIcon(request):	
	name=request.data.get("name")
	fields=request.data.get("fields")	
	image=request.data.get("image")
	icon=IconBase.objects.create(name=name, field=fields, thumbnail=image)
	try:
		categoryId=int(request.data.get("category"))
		category=Category.objects.get(id=categoryId)
		icon.category=category
		icon.save(user=request.user)
	except:
		print("WITHOUT CATEGORY")
		pass

	return Response(status=HTTP_200_OK)

@api_view(['POST'])
def EditCategory(request):
	data=json.loads(request.data['data'])
	thumbnail=request.data['thumbnail']
	name=data['name']
	ids=data['id']
	icons=data['icons']
	category=Category.objects.get(id=ids)
	cIconBase=IconBase.objects.filter(category=category)

	#Removing all icon from category
	for x in cIconBase:
		x.category=None
		x.save()

	#Adding new icons to category
	for x in icons:
		iconBase=IconBase.objects.get(id=x['id'])
		iconBase.category=category
		iconBase.save()

	category.name=name
	category.thumbnail=thumbnail
	category.save()

	return Response(status=HTTP_200_OK)

@api_view(['POST'])
def EditIcon(request):
	name=request.data.get("name")
	fieldsStr=request.data.get("fields")	
	fields=json.loads(fieldsStr)
	image=request.data.get("image")	
	ids=request.data.get("id")
	iconBase=IconBase.objects.get(id=ids)
	try:
		categoryId=int(request.data.get("category"))
		category=Category.objects.get(id=categoryId)
		iconBase.category=category
		iconBase.save()
	except:
		pass

	iconBase.name=name
	iconBase.save()
	if image!="undefined":
		iconBase.image=image
		iconBase.save()

	if len(fields)!=0:
		iconBase.field=fieldsStr
		iconBase.save()

	return Response(status=HTTP_200_OK)

@api_view(['POST'])
def GetProjectIcons(request):
	project=Project.objects.get(id=request.data)
	categories=Category.objects.all()
	icons=IconBase.objects.filter(category__isnull=True)

	selectedIcon=IconBase.objects.filter(project=project)

	serializer=CategorySerializer(categories, many=True)
	serializerIcon=IconBaseSerializer(icons, many=True)
	serializerSelectedIcon=IconBaseSerializer(selectedIcon, many=True)

	res={
		"categories":serializer.data,
		"unsortedIcons":serializerIcon.data,
		"selectedIcons":serializerSelectedIcon.data
	}
	return Response(res, status=HTTP_200_OK)

@api_view(['POST'])
def AddSelectedIcon(request):
	projectID=request.data['projectID']
	selectedIcons=request.data['selectedIcons']
	project=Project.objects.get(id=projectID)

	projectIcon=IconBase.objects.filter(project=project)

	#Removing all icons from a project
	for x in projectIcon:
		x.project.remove(project)
		x.save()

	for x in selectedIcons:
		iconBase=IconBase.objects.get(id=x['id'])
		iconBase.project.add(project)
		iconBase.save()

	return Response(status=HTTP_200_OK)

@api_view(['POST'])
def DeleteCategory(request):
	ids=int(request.data)
	Category.objects.get(id=ids).delete()
	return Response(status=HTTP_200_OK)

@api_view(['POST'])
def DeleteIconBase(request):
	ids=int(request.data)
	IconBase.objects.get(id=ids).delete()
	return Response(status=HTTP_200_OK)

@api_view(['POST'])
def SubmitForm(request): 
	res=dict(request.data.lists())
	profile=request.user.profile
	report=request.data['report']
	projID=request.data['proj_id']
	iconString=request.data['icon']
	iconID=request.data['iconID']
	icon=Icon.objects.get(iconid=iconID)

	project=Project.objects.get(id=projID)

	managerEmail=[]
	for x in project.accountManager.all():
		managerEmail.append(x.email)

	if profile.isClient:
		managerEmail.append(profile.email)
		icon.senderReportEmail=profile.email

	subject=project.name+" #"+str(project.number)
	content=iconString+"<br/>"+report+"<br/><br/>"+profile.first_name+" "+profile.last_name
	email = EmailMessage(subject, content, to=managerEmail)             
	email.content_subtype = "html" 

	try:
		pictures=res['pictures']
		for x in pictures:
			if x.name.endswith(".pdf"):
				email.attach(x.name, x.file.read(), "application/pdf")
			elif x.name.endswith(".jpeg") or x.name.endswith(".jpg"):
				email.attach(x.name, x.file.read(), "image/jpeg")
			elif x.name.endswith(".png"):
				email.attach(x.name, x.file.read(), "image/png")
			else:
				email.attach(x.name, x.file.read(), "image/jpeg")
	except: pass

	try:
		audio=request.data['audio']
		email.attach(audio.name, audio.file.read(), "audio/mpeg")
	except: pass	
	email.send()
	icon.isReported=True
	
	icon.save(user=request.user)
	return Response("success",status=HTTP_200_OK)

@api_view(['POST'])
def SaveNewIcon(request):
	x=json.loads(request.data['icon'])
	survey_id=request.data['survey_id']
	survey=Survey.objects.get(id=survey_id)
	print("SAVE NEW ICON")
	try:
		iconBase=IconBase.objects.get(id=int(x['iconBaseID']))
		thumbnail=iconBase.thumbnail
	except:
		iconBase=None
		icon=Icon.objects.get(iconid=x['iconID'])
		thumbnail=icon.thumbnail

	try:
		icon=Icon.objects.create(iconid=x['id'],
			survey=survey,
			name=x['name'],
			order=x['order'], 
			angle=x['angle'], 			
			depth=x['depth'], 
			opacity=x['trans'], 
			iconRotate=x['iconRotate'],
			color=x['color'], 
			bgColor=x['bgColor'],
			rotate=x['direction'], 
			xposition=x['xposition'], 
			yposition=x['yposition'],
			isLocked=x['isLocked'],
			unit=x['unit'],			
			iconBase=iconBase,	
			thumbnail=thumbnail,
			answer=str(x['info']['fields'])
			)
	except:pass

	return Response("success",status=HTTP_200_OK)

@api_view(['POST'])
def SaveNewCable(request):
	x=json.loads(request.data['cable'])
	survey_id=request.data['survey_id']
	survey=Survey.objects.get(id=survey_id)	
	icon=Icon.objects.get(iconid=x['iconParent'])	
	cable=Cable.objects.create(iconid=x['id'],
		survey=survey,
		name=x['name'],
		depth=x['depth'],
		color=x['color'],
		isLocked=x['isLocked'],
		unit=x['unit'],
		answer=x['info']['fields'],
		order=x['order'],
		iconParent=icon
	)

	newLine=json.loads(request.data['newLine'])
	Section.objects.create(sectionid=newLine['id'], x1=newLine['x1'], x2=newLine['x2'], y1=newLine['y1'], y2=newLine['y2'], depth=newLine['depth'], cable=cable,		
	answer=newLine['info']['fields'], cableID=cable.iconid, unit="feet")

	return Response("success",status=HTTP_200_OK)

@api_view(['POST'])
def HandleLock(request):
	data=request.data 
	if data['type']=="icon":
		element=Icon.objects.get(iconid=data['id'])
	elif data['type']=="cable":
		element=Cable.objects.get(iconid=data['id'])

	element.isLocked=json.loads(data['isLocked'])
	element.save()
	return Response("success",status=HTTP_200_OK)

@api_view(['POST'])
def AddLine(request):
	newLine=json.loads(request.data['newLine'])
	cableID=request.data['cableID']
	cable=Cable.objects.get(iconid=cableID)
	namme=cable.name
	cableLines=Section.objects.filter(cable=cable)
	Section.objects.create(
		sectionid=newLine['id'],
		cableID=cableID, 
		x1=newLine['x1'], 
		x2=newLine['x2'], 
		y1=newLine['y1'], 
		y2=newLine['y2'], 
		unit="feet",
		depth=newLine['depth'], 
		cable=cable, 
		order=newLine['order'], 
		answer=newLine['info']['fields'])

	return Response("success",status=HTTP_200_OK)

@api_view(['POST'])
def SaveLine(request):
	lines=json.loads(request.data['lines'])
	cableID=request.data['cableID']
	cable=Cable.objects.get(iconid=cableID)
	survey=cable.survey
	if len(lines)==0:		
		cable.delete()
		for order, cable in enumerate(Cable.objects.filter(survey=survey)):
			cable.order=order+1
			cable.save()
	else:
		cableLines=Section.objects.filter(cable=cable)
		for line in lines:
			try:
				linne=cableLines.get(sectionid=line['id'])
				linne.x1=line['x1']
				linne.x2=line['x2']
				linne.y1=line['y1']
				linne.y2=line['y2']
				linne.order=line['order']
				linne.depth=line['depth']
				linne.save()
			except:pass
		try:
			if request.data['isLocked']=="true":
				isLocked=True
			else:
				isLocked=False
			cable.isLocked=isLocked
		except:pass

		#Delete Section
		try:
			deletedSectionId=request.data['deletedSectionId']
			cableToChangeId=request.data['cableToChangeId']
			sectionToDelete=Section.objects.get(sectionid=deletedSectionId)
			sectionToChange=Section.objects.get(sectionid=cableToChangeId)
			sectionToChange.x1=sectionToDelete.x1
			sectionToChange.x2=sectionToDelete.x2
			sectionToChange.y1=sectionToDelete.y1
			sectionToChange.y2=sectionToDelete.y2
			sectionToChange.save()
			sectionToDelete.delete()
		except:
			try:
				deletedSectionId=request.data['deletedSectionId']
				sectionToDelete=Section.objects.get(sectionid=deletedSectionId)
				sectionToDelete.delete()
			except:pass

		cable.save()
	try:
		totalLength=request.data['totalLength']
		cable.depth=totalLength
		cable.save()
	except:pass

	return Response("success",status=HTTP_200_OK)

@api_view(["POST"])
def ChangePosition(request):	
	data=json.loads(request.data['data'])
	icon=Icon.objects.get(iconid=data["id"])
	icon.xposition=data["xpos"]
	icon.yposition=data['ypos']
	icon.save(user=request.user)
	return Response("success",status=HTTP_200_OK)

@api_view(["POST"])
def DeleteIcon(request):
	data=request.data
	iconn=Icon.objects.get(iconid=data)
	surv=iconn.survey
	name=iconn.name
	oldOrder=iconn.order
	iconn.delete()

	#Reorder icon's order in the same survey
	for icon in surv.icon.filter(name=name):
		if(icon.order-1==oldOrder):			
			icon.order=oldOrder
			icon.save(user=request.user)
			oldOrder+=1

	return Response("success",status=HTTP_200_OK)

@api_view(["POST"])
def IconAttributeChange(request):
	ids=json.loads(request.data['id'])
	data=json.loads(request.data['data'])
	icon=Icon.objects.get(iconid=ids)
	icon.angle=data['angle']
	icon.opacity=data['trans']
	icon.rotate=data['direction']
	icon.depth=data['depth']
	icon.color=data['color']
	icon.bgColor=data['bgColor']
	icon.isLocked=data['isLocked']
	icon.iconRotate=data['iconRotate']
	icon.unit=data['unit']
	icon.survey.iconSize=data['iconSize']
	icon.save(user=request.user)
	return Response("success",status=HTTP_200_OK)

@api_view(["POST"])
def HandleResolve(request):
	data=request.data
	icon=Icon.objects.get(iconid=data['iconID'])
	project=Project.objects.get(id=data['projectID'])

	managerEmail=[]
	for x in project.accountManager.all():
		managerEmail.append(x.email)

	if icon.senderReportEmail:
		managerEmail.append(icon.senderReportEmail)

	subject=project.name+" #"+str(project.number)
	content=icon.name + "#" + str(icon.order)+" is resolved"
	email = EmailMessage(subject, content, to=managerEmail)             
	email.content_subtype = "html" 
	email.send()

	icon.isReported=False
	icon.save(user=request.user)
	return Response("success",status=HTTP_200_OK)

@api_view(["POST"])
def SubmitLabel(request):
	data=request.data
	cable=Cable.objects.get(iconid=data['cableID'])
	cable.label=data['label']
	cable.save()
	return Response("success",status=HTTP_200_OK)

@api_view(["POST"])
def DelPhoto(request):
	data=request.data
	if settings.MAIN:
		url="https://main.wiseeyes.link/media/"
	else:
		url="http://127.0.0.1:8000/media/"
	data = data.replace(url, "")
	iconPicture=IconPicture.objects.get(picture__exact=data).delete()
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def AddPhoto(request):
	data=request.data
	icon=Icon.objects.get(iconid=data['iconID'])
	iconPicture=IconPicture.objects.create(picture=data['pic'])
	iconPicture.icon=icon
	iconPicture.save()
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def EditSurvToolbar(request):
	data=request.data
	iconID=data['iconID']
	icon=Icon.objects.get(iconid=iconID)
	if data['type']=="dataChange":
		icon.surveyToolbar=data['data']
	elif data['type']=="audio":
		if data['audio']!="null":
			icon.audioInfo=data['audio']
			icon.save(user=request.user)
		icon.audioFile.delete()
		icon.save(user=request.user)
		icon.audioFile=data['audioBlob']

	icon.save(user=request.user)
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def EditInsToolbar(request):
	data=request.data
	iconID=data['iconID']
	icon=Icon.objects.get(iconid=iconID)
	if data['type']=="dataChange":
		icon.installationToolbar=data['data']
		icon.save(user=request.user)
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def SaveField(request):
	data=request.data
	iconID=data['iconID']
	icon=Icon.objects.get(iconid=iconID)
	icon.answer=data['data']
	icon.save(user=request.user)
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def AddComment(request):
	data=request.data
	iconID=data['iconID']
	icon=Icon.objects.get(iconid=iconID)
	icon.comments=data['data']
	icon.save(user=request.user)
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def SaveIconSize(request):
	data=request.data
	survey=Survey.objects.get(id=int(data['surveyID']))
	survey.iconSize=int(data['data'])
	survey.save()
	return Response("Success", status=HTTP_200_OK)

def FetchAllCamera(request, surveyID):
	req=surveyID
	iconAll=Icon.objects.all()
	for x in iconAll:
		paricture=x.thumbnail
		imagge=Image.open(paricture)
		max_size=(150,150)
		imagge.thumbnail(max_size)
		imagge.save(paricture.path)

	survey=Survey.objects.get(id=req)
	icons=Icon.objects.filter(survey=survey)
	cables=Cable.objects.filter(survey=survey).prefetch_related("section")
	newArrayCables=[]
	newArraySections=[]
	if settings.MAIN:
		url="https://main.wiseeyes.link"
	else:
		url="http://127.0.0.1:8000"
	for x in cables:	
		sections=Section.objects.filter(cableID=x.iconid)
		for y in sections:
			pic_list=[]

			for q in y.sectionPicture.all():			
				pic_url=url+request.build_absolute_uri(q.picture.url)
				pic_list.append(pic_url)

			if y.audioInfo:
				audio_info=json.loads(y.audioInfo)
				audio_dummy={
					'blobURL':url+request.build_absolute_uri(y.audioFile.url),
					'startTime':audio_info['startTime'],
					'stopTime':audio_info['stopTime'],
					'options':audio_info['options']
				}
			else:
				audio_dummy=None
			if y.answer:
				arrayInfo = ast.literal_eval(y.answer)
			else:
				arrayInfo=[]
			dummySection={
				"id":y.sectionid,
				"name":y.name,
				"depth":y.depth,
				"unit":y.unit,
				"order":y.order,
				"cableID":x.iconid,
				"isReported":y.isReported,
				"label":x.label,
				"pathType":y.pathType,
				"note":y.note,
				"x1":y.x1,
				"x2":y.x2,
				"y1":y.y1,
				"y2":y.y2,
				"senderReportEmail":y.senderReportEmail,
				'info':{
					'fields':arrayInfo,
					'pictures':pic_list,
					'audio':audio_dummy
				},
				'addInfo':{
					'startDate':y.startDate,
					'endDate':y.endDate,
					'techName':y.techName,
					'test':y.test,
					'comment':y.comment,
				}
			}
			newArraySections.append(dummySection)

		if x.answer:
			arrayInfo = ast.literal_eval(x.answer)
		else:
			arrayInfo=[]

		dummy={
			'id':x.iconid,
			'name':x.name,
			'color':x.color,
			'depth':x.depth,
			'unit':x.unit,
			'isLocked':x.isLocked,	
			'label':x.label,
			'order':x.order,
			"field":arrayInfo
		}
		newArrayCables.append(dummy)

	newArrayIcons=[]
	for x in icons:
		pic_list=[]
		for y in x.iconPicture.all():			
			pic_url=url+request.build_absolute_uri(y.picture.url)
			pic_list.append(pic_url)
		if x.audioInfo:
			audio_info=json.loads(x.audioInfo)
			audio_dummy={
				'blobURL':url+request.build_absolute_uri(x.audioFile.url),
				'startTime':audio_info['startTime'],
				'stopTime':audio_info['stopTime'],
				'options':audio_info['options']
			}
		else:
			audio_dummy=None
		arrayInfo = ast.literal_eval(x.answer)

		if x.surveyToolbar:
			surveyToolbar=x.surveyToolbar
		else:
			surveyToolbar=""

		if x.installationToolbar:
			installationToolbar=x.installationToolbar
		else:
			installationToolbar=""

		if x.comments:			
			comments=x.comments
		else:
			comments=""

		iconBBase=""
		if x.iconBase:
			iconBBase=x.iconBase.id
		dummy={
			'id':x.iconid,
			'name':x.name,
			'order':x.order,
			'xposition':x.xposition,
			'yposition':x.yposition,
			'direction':x.rotate,
			'trans':x.opacity,
			'color':x.color,
			'bgColor':x.bgColor,
			'iconRotate':x.iconRotate,
			'angle':x.angle,
			'depth':x.depth,
			'unit':x.unit,
			'isLocked':x.isLocked,
			'image':url+x.thumbnail.url,
			'iconBaseID':iconBBase,
			'dateUpdated':x.dateUpdated,
			'isReported':x.isReported,	
			'surveyToolbar':surveyToolbar,
			'installationToolbar':installationToolbar,	
			'comments':comments	,
			'info':{
				'fields':arrayInfo,
				'pictures':pic_list,
				'audio':audio_dummy
			},
			'addInfo':{
				'startDate':x.startDate,
				'endDate':x.endDate,
				'techName':x.techName,
				'test':x.test,
				'comment':x.comment,
			}
		}
		newArrayIcons.append(dummy)
	res={
		"icons":newArrayIcons,
		"cables":newArrayCables,
		"lines":newArraySections
	}

	return res

@api_view(["POST"])
def CategoryOrder(request):
	data=request.data
	for x in data:
		category=Category.objects.get(id=x['id'])
		category.priority=x['index']
		category.save()
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def ChangeImage(request):	
	data=request.data
	survey=Survey.objects.get(id=int(data['surveyID']))
	survey.picture=data['selectedFile']
	survey.distance=float(data['distance'])
	survey.pixelDistance=float(data['pixelDistance'])
	survey.unit=data['unit']
	survey.save()
	return Response("success",status=HTTP_200_OK)


@api_view(["POST"])
def CreateSaveSurvey(request):	
	data=request.data	
	survey=Survey.objects.get(uid=data['surveyUID'])

	icons=survey.icon.prefetch_related('iconPicture').all()

	newPic=DuplicateImage(survey.picture.name,survey.picture)

	survey.pk=None
	survey.uid=uuid.uuid4()
	survey.picture=newPic
	survey.stageStatus="next"
	survey.version="alternate"
	survey.save()	
	SavedSurvey.objects.create(name=data['text'], mainSurveyID=survey.name, survey=survey, editedProfile=request.user.profile, project=survey.project)
	for y in icons:
		iconPictures=y.iconPicture.all()
		y.pk=None
		randomId=randint(10000000000, 99999999999)
		y.iconid=str(randomId)
		y.project=survey.project
		y.save()
		for z in iconPictures:
			z.pk=None
			z.icon=y
			z.save()

	return Response(survey.id,status=HTTP_200_OK)

@api_view(["POST"])
def HandleOverwrite(request):	
	data=request.data
	survey1=Survey.objects.get(id=data['survIDReplace'])
	survey2=Survey.objects.get(id=data['survID'])
	savedSurvey2=survey2.savedSurvey.all()[0]

	icons=survey1.icon.prefetch_related('iconPicture').all()
	newPic=DuplicateImage(survey1.picture.name,survey1.picture)

	survey1.pk=None
	survey1.uid=uuid.uuid4()
	survey1.stage=survey2.stage
	survey1.version=survey2.version
	survey1.picture=newPic
	survey1.save()

	savedSurvey2.survey=survey1
	savedSurvey2.save()

	survey2.delete()

	for y in icons:
		iconPictures=y.iconPicture.all()
		y.pk=None
		randomId=randint(10000000000, 99999999999)
		y.iconid=str(randomId)
		y.project=survey1.project
		y.save()
		for z in iconPictures:
			z.pk=None
			z.icon=y
			z.save()

	return Response("success",status=HTTP_200_OK)