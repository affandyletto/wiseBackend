from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_403_FORBIDDEN,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK,
	HTTP_401_UNAUTHORIZED
)
from User.permissions import requirePermissionsViews
from User.models import Profile
from User.serializers import ProfileSerializer, ProfileSerializer2
from .serializers import ProjectSerializer, ProjectDetailSerializer, AttachmentSerializer, TicketListSerializer, TicketSerializer
from Organization.models import ClientOrganization, Organization
from Organization.serializers import CompanySerializer, ClientOrgSerializer
from .models import Project, Attachment, Ticket, TicketPicture, ChatFile
import json
from datetime import datetime
import ast
from random import randint
from django.core.files.base import ContentFile
from Survey.models import Survey, IconBase, Icon, Category, SavedSurvey
from Survey.views import FetchAllCamera
import os
from django.conf import settings
from xlsxwriter.workbook import Workbook
import io
import pandas as pd
import csv
from django.db.models import Q
from Survey.serializers import IconBaseSerializer, SurveySerializer, CategorySerializer, IconSerializer
from django.db.models import Count
from io import BytesIO
import random
from django.core.mail import EmailMessage
from django.db import transaction
import uuid
from .helper import DuplicateImage, DuplicateSurvey

@api_view(['GET'])
def LoadClient(request):
	profile=request.user.profile

	if profile.company:
		company=profile.company
		profiles=Profile.objects.select_related('User').filter(company=company, isClient=True)
		clientOrganizations=ClientOrganization.objects.filter(company=company)

		if profile.isSuperAdmin or profile.isCompanyAdmin:
			projects=Project.objects.filter(company=company)
		elif profile.isAccountManager or profile.isSurveyor or profile.isDesigner or profile.isProposal or profile.isTechnician:
			projects=Project.objects.filter(Q(company=company), Q(accountManager=profile) | Q(surveyer=profile) | Q(designer=profile) | Q(proposal=profile) | Q(technician=profile))
		elif profile.isClient:
			projects=Project.objects.filter(company=company, client=profile, stage="as built")
		elif profile.isFreeUser:
			projects=Project.objects.filter(company=company, stage__in=['profile','survey','design'])

	elif not profile.company:
		profiles=[]
		clientOrganizations=[]
		projects=[]

	serializerProfile=ProfileSerializer(profiles, many=True)		
	serializerCompanyClient=ClientOrgSerializer(clientOrganizations, many=True)
	serializerCompany=CompanySerializer(company, many=False)	
	serializerProject=ProjectSerializer(projects, many=True)
	resData={
		'profiles':serializerProfile.data,
		'clientOrganizations':serializerCompanyClient.data,
		'organization':serializerCompany.data,
		'projects':serializerProject.data
	}
	return Response(resData, status=HTTP_200_OK)

'''
@api_view(['POST'])
def OnSelectOrganization(request):
	data=request.data
	profile=request.user.profile

	#Force log out if the user's role was changed
	if profile.isPrevilageChange==True:
		profile.isPrevilageChange=False
		profile.save()
		res={
			"message":"Your role was changed, please login again"
		}
		return Response(res, status=HTTP_200_OK)

	company=Organization.objects.prefetch_related("profile_set").get(id=data)
	profiles=Profile.objects.select_related('User').prefetch_related("company").select_related("clientOrg").filter(company=company, isClient=True)
	clientOrganizations=ClientOrganization.objects.select_related("company").filter(company=company)

	if profile.isSuperAdmin or profile.isCompanyAdmin or profile.isAccountManager:
		projects=Project.objects.prefetch_related("clientOrg").filter(company=company)
	elif profile.isClient:
		projects=Project.objects.prefetch_related("clientOrg").filter(company=company, client=profile, stage="as built")
	else:
		projects=Project.objects.prefetch_related("clientOrg").filter(Q(company=company), (Q(surveyer=profile)&Q(stage__in=["profile","survey"])) | (Q(designer=profile)&Q(stage="design")) | (Q(proposal=profile)&Q(stage="estimate")) | (Q(technician=profile)&Q(stage="deployment"))).distinct()
	
	serializerProfile=ProfileSerializer(profiles, many=True)		
	serializerCompanyClient=ClientOrgSerializer(clientOrganizations, many=True)
	serializerCompany=CompanySerializer(company, many=False)	
	serializerProject=ProjectSerializer(projects, many=True)
	res={
		'profiles':serializerProfile.data,
		'clientOrganizations':serializerCompanyClient.data,
		'organization':serializerCompany.data,
		'projects':serializerProject.data
	}
	return Response(res, status=HTTP_200_OK)
'''

@api_view(['POST'])
def OnSelectOrganization(request):
	data = request.data
	profile = request.user.profile

	# Force log out if the user's role was changed
	if profile.isPrevilageChange:
		profile.isPrevilageChange = False
		profile.save()
		res = {
			"message": "Your role was changed, please login again"
		}
		return Response(res, status=HTTP_200_OK)

	company = get_object_or_404(Organization.objects.prefetch_related("profile_set"), id=data)
	profiles = Profile.objects.select_related('User').prefetch_related("company").select_related("clientOrg").filter(company=company, isClient=True)
	client_organizations = ClientOrganization.objects.select_related("company").filter(company=company)
	
	
	if profile.isSuperAdmin or profile.isCompanyAdmin or profile.isAccountManager:
		projects = Project.objects.prefetch_related("clientOrg").filter(company=company).distinct()
		tickets=Ticket.objects.filter(company=company, seenByAdmin=False)
	elif profile.isClient:
		projects = Project.objects.prefetch_related("clientOrg").filter(company=company, client=profile, stage="as built")
		tickets=Ticket.objects.filter(company=company, seenByClient=False, client=profile)
	else:
		projects = Project.objects.prefetch_related("clientOrg").filter(Q(company=company), (Q(surveyer=profile)&Q(stage__in=["profile","survey"])) | (Q(designer=profile)&Q(stage="design")) | (Q(proposal=profile)&Q(stage="estimate")) | (Q(technician=profile)&Q(stage="deployment"))).distinct()

	serializer_profile = ProfileSerializer(profiles, many=True)
	serializer_client_organizations = ClientOrgSerializer(client_organizations, many=True)
	serializer_company = CompanySerializer(company)
	serializer_projects = ProjectSerializer(projects, many=True)
	res = {
		'unseenTicket':len(tickets),
		'profiles': serializer_profile.data,
		'clientOrganizations': serializer_client_organizations.data,
		'organization': serializer_company.data,
		'projects': serializer_projects.data
	}

	return Response(res, status=HTTP_200_OK)

@api_view(["POST"])
def FetchAllData(request):
	orgId=request.data['data']
	projIds=request.data['projIds']
	survIds=request.data['survData']
	profile=request.user.profile

	#Force log out if the user's role was changed 
	if profile.isPrevilageChange==True:
		profile.isPrevilageChange=False
		profile.save()
		res={
			"message":"Your role was changed, please login again"
		}
		return Response(res, status=HTTP_200_OK)	

	company=Organization.objects.prefetch_related("profile_set").get(id=orgId)
	profiles=Profile.objects.select_related('User').prefetch_related("company").select_related("clientOrg").filter(company=company, isClient=True)
	clientOrganizations=ClientOrganization.objects.select_related("company").filter(company=company)

	projects=Project.objects.filter(id__in=projIds)

	'''
	if profile.isSuperAdmin or profile.isCompanyAdmin or profile.isAccountManager:
		projects=Project.objects.prefetch_related("clientOrg").filter(company=company)
	elif profile.isClient:
		projects=Project.objects.prefetch_related("clientOrg").filter(company=company, client=profile, stage="as built")
	else:
		projects=Project.objects.prefetch_related("clientOrg").filter(Q(company=company), (Q(surveyer=profile)&Q(stage__in=["profile","survey"])) | (Q(designer=profile)&Q(stage="design")) | (Q(proposal=profile)&Q(stage="estimate")) | (Q(technician=profile)&Q(stage="deployment"))).distinct()
	'''	

	categories=Category.objects.all()
	categorySerializer=CategorySerializer(categories, many=True)
	surveys=Survey.objects.filter(id__in=survIds)
	newSurrv=[]

	for x in surveys:
		newSurv=DuplicateSurvey(x,x.stage,x.stageStatus, profile, "offline")
		newSurrv.append(newSurv)
	newSurveys=Survey.objects.filter(id__in=newSurrv)

	icons=IconBase.objects.filter(project__in=projects)
	serializerProfile=ProfileSerializer(profiles, many=True)		
	serializerCompanyClient=ClientOrgSerializer(clientOrganizations, many=True)
	serializerCompany=CompanySerializer(company, many=False)	
	serializerProject=ProjectSerializer(projects, many=True)
	serializerProjectsDetails=ProjectDetailSerializer(projects, many=True)
	serializerIconBase=IconBaseSerializer(icons, many=True)
	serializerSurvey=SurveySerializer(surveys, many=True)
	res={
		'profiles':serializerProfile.data,
		'clientOrganizations':serializerCompanyClient.data,
		'organization':serializerCompany.data,
		'projects':serializerProject.data,
		'projectsDetails':serializerProjectsDetails.data,
		'surveys':serializerSurvey.data,
		'iconBase':serializerIconBase.data,		
		'categories':categorySerializer.data,
		'newSurvId':newSurrv
	}

	return Response(res, status=HTTP_200_OK)

#Fetch all Icons, Cables, Lines from each survey
@api_view(["POST"])
def FetchAllSurveyData(request):
	compids=request.data['data']
	projIds=request.data['projIds']
	survIds=request.data['survData']
	profile=request.user.profile
	company=Organization.objects.prefetch_related("profile_set").get(id=compids)
	projects=Project.objects.filter(id__in=projIds)

	'''
	if profile.isSuperAdmin or profile.isCompanyAdmin or profile.isAccountManager:
		projects=Project.objects.prefetch_related("clientOrg").filter(company=company)
	elif profile.isClient:
		projects=Project.objects.prefetch_related("clientOrg").filter(company=company, client=profile, stage="as built")
	else:
		projects=Project.objects.prefetch_related("clientOrg").filter(Q(company=company), (Q(surveyer=profile)&Q(stage__in=["profile","survey"])) | (Q(designer=profile)&Q(stage="design")) | (Q(proposal=profile)&Q(stage="estimate")) | (Q(technician=profile)&Q(stage="deployment"))).distinct()
	'''
	surveys=Survey.objects.filter(id__in=survIds)
	surveyData=[]
	for survey in surveys:
		qwesz=FetchAllCamera(request, survey.id)
		surveyData.append({'surveyID':survey.id,'icons':qwesz['icons'],'cables':qwesz['cables'],'lines':qwesz['lines']})

	return Response({'surveyData':surveyData}, status=HTTP_200_OK)

@api_view(['POST'])
@requirePermissionsViews("SuperAdmin", "CompanyAdmin", "AccountManager")
def RegisterProject(request):
	data=request.data
	org=Organization.objects.get(id=data["organization_id"])
	new_project=Project.objects.create(name=data['name'],number=data['projectNum'], company=org)
	for x in data['client_org_id']:
		clientOrg=ClientOrganization.objects.get(id=x)
		new_project.clientOrg.add(clientOrg)
	for x in data['client_user_id']:
		clientUser=Profile.objects.get(id=x)
		new_project.client.add(clientUser)

	new_project.save()
	
	return Response("success", status=HTTP_200_OK)

@api_view(["POST"])
@requirePermissionsViews("SuperAdmin", "AccountManager", "CompanyAdmin", 'Technician')
def EditProjectClient(request):
	data=request.data
	proj=Project.objects.get(id=data['id'])
	allClient=proj.client.all()

	#Checking ig the number is exist
	Projj=Project.objects.filter(number=int(data['number']))	
	if len(Projj)>1:
		return Response("Project number exist, please select another number",status=HTTP_200_OK)

	for x in allClient:
		if x.id not in data['client']:
			proj.client.remove(x)
			proj.save()
	for x in data['client']:
		client=Profile.objects.get(id=x)
		if client not in allClient:
			proj.client.add(client)
			proj.save()

	proj.name=data['name']
	proj.number=data['number']
	proj.save()

	return Response("success", status=HTTP_200_OK)

@api_view(["POST"])
@requirePermissionsViews("SuperAdmin", "AccountManager", "CompanyAdmin", 'Technician')
def EditProject(request):
	data=request.data
	proj=Project.objects.get(id=data['id'])
	allClient=proj.client.all()
	allClientOrg=proj.clientOrg.all()
	#Checking ig the number is exist
	Projj=Project.objects.filter(number=int(data['number']))
	if len(Projj)>0 and Projj[0].id!=proj.id:
		print("PROJECT NUMBER EXIST")
		return Response("Project number exist, please select another number",status=HTTP_200_OK)

	#Remove existing client in a project
	for x in allClient:
		if x.id not in data['client']:
			proj.client.remove(x)
			proj.save()

	for x in allClientOrg:
		if x.id not in data['clientOrg']:
			proj.clientOrg.remove(x)
			proj.save()

	#Add client to a project
	for x in data['client']:
		client=Profile.objects.get(id=x)
		if client.id not in allClient:
			proj.client.add(client)
			proj.save()

	for x in data['clientOrg']:
		clientOrg=ClientOrganization.objects.get(id=x)
		if clientOrg.id not in allClientOrg:
			proj.clientOrg.add(clientOrg)
			proj.save()

	proj.name=data['name']
	proj.number=data['number']
	proj.save()

	'''
	try:
		clientOrgs=data['clientOrg']	
		clientOrg=ClientOrganization.objects.get(id=clientOrgs['id'])
	except:
		clientOrg=None

	del data['clientOrg']
	
	comp=proj.update(**data, clientOrg=clientOrg)	
	'''
	res={
		"type":"success",
		"message":"Company edited"
	}
	return Response(res, status=HTTP_200_OK)

@api_view(["POST"])
def GetProject(request):
	profile=request.user.profile
	projectID=request.data
	project=Project.objects.prefetch_related('accountManager','surveyer','designer','proposal','technician').get(id=projectID)
	clientOrganizations=ClientOrganization.objects.filter(company=project.company)
	serializerCompanyClient=ClientOrgSerializer(clientOrganizations, many=True)
	serializerProjectDetail=ProjectDetailSerializer(project, many=False)

	allAccountManager=project.accountManager.all()
	allSurveyer=project.surveyer.all()
	allDesigner=project.designer.all()
	allProposal=project.proposal.all()
	allTechnician=project.technician.all()
	allClient=project.client.all()

	res={
		'project':serializerProjectDetail.data,
		'clientOrgs':serializerCompanyClient.data
	}
	if not profile.isSuperAdmin:
		companies=profile.company.all()		
		if project.company not in companies:
			return Response("FORBIDDEN", status=HTTP_403_FORBIDDEN)

		if (profile in allSurveyer and (project.stage=="profile" or project.stage=="survey")) or (profile in allDesigner and project.stage=="design") or (profile in allProposal and project.stage=="estimate") or (profile in allTechnician and project.stage=="deployment") or (profile in allClient and project.stage=="as built"):			
			return Response(res, status=HTTP_200_OK)
		elif profile.isFreeUser:
			if project.stage not in ['profile','survey','design']:
				return Response("FORBIDDEN", status=HTTP_403_FORBIDDEN)
			else:
				return Response(res, status=HTTP_200_OK)
		elif profile.isCompanyAdmin or profile.isAccountManager:
			return Response(res, status=HTTP_200_OK)
		else:
			return Response("FORBIDDEN", status=HTTP_403_FORBIDDEN)				
	
	return Response(res, status=HTTP_200_OK)

@api_view(["POST"])
@requirePermissionsViews("SuperAdmin", "AccountManager", "CompanyAdmin", 'Technician')
def EditProjectInfo(request):
	typpe=request.data.get('type')
	ids=request.data.get('id')
	project=Project.objects.filter(id=ids)
	oneProject=Project.objects.get(id=ids)
	if typpe=="projectInfo":
		data=json.loads(request.data.get('data'))		
		project.update(**data)
		serializer=ProjectDetailSerializer(project[0], many=False)
		return Response(serializer.data, status=HTTP_200_OK)
	elif typpe=="startDate":
		data=json.loads(request.data.get('data'))
		try:
			date=datetime.strptime(data,"%Y-%m-%d").date()
		except:
			date=None
		oneProject.startDate=date
		oneProject.save()
		serializer=ProjectDetailSerializer(oneProject, many=False)
		return Response(serializer.data, status=HTTP_200_OK)
	elif typpe=="endDate":
		data=json.loads(request.data.get('data'))
		try:
			date=datetime.strptime(data,"%Y-%m-%d").date()
		except:
			date=None
		oneProject.endDate=date
		oneProject.save()
		serializer=ProjectDetailSerializer(oneProject, many=False)
		return Response(serializer.data, status=HTTP_200_OK)
	elif typpe=="hibernate":
		data=json.loads(request.data.get('data'))
		try:
			date=datetime.strptime(data,"%Y-%m-%d").date()
		except:
			date=None
		oneProject.hibernate=date
		oneProject.save()
		serializer=ProjectDetailSerializer(oneProject, many=False)
		return Response(serializer.data, status=HTTP_200_OK)
	elif typpe=="changeClient":
		clientOrg=ClientOrganization.objects.get(id=json.loads(request.data.get('data')))
		oneProject.clientOrg.set(clientOrg)
		oneProject.save()
		serializer=ProjectDetailSerializer(oneProject, many=False)
		return Response(serializer.data, status=HTTP_200_OK)
	elif typpe=="subCategory":
		data=json.loads(request.data.get('data'))
		oneProject.subCategory=data
		oneProject.save()
		serializer=ProjectDetailSerializer(oneProject, many=False)
		return Response(serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def EditStage(request):
	project=Project.objects.get(id=request.data.get('id'))
	typpe=request.data.get("type")
	stages=ast.literal_eval(project.stageHistory)	

	#Copy the surveys from previous stage to next stage
	if typpe=="next":			
		if project.stage=="profile":
			project.stage="survey"
			stages.append("survey")			
			project.stageHistory=stages
			project.stageStatus="next"
			project.subCategory=""
			filteredSurvey=project.survey.filter(stage="profile", stageStatus="next", version="main").prefetch_related('icon')
			#Copy the survey with all it's icons
			for x in filteredSurvey:
				DuplicateSurvey(x, "survey","next",request.user.profile,'main')				

		elif project.stage=="survey":
			project.stage="design"
			stages.append("design")
			project.stageHistory=stages
			filteredSurvey=project.survey.filter(stage="survey", stageStatus="next", version="main").prefetch_related('icon')
			for x in filteredSurvey:
				DuplicateSurvey(x, "design","next",request.user.profile,'main')				

		elif project.stage=="design":
			project.stage="estimate"
			stages.append("estimate")
			project.stageHistory=stages
			filteredSurvey=project.survey.filter(stage="design", stageStatus="next", version="main").prefetch_related('icon')
			for x in filteredSurvey:
				DuplicateSurvey(x, "estimate","next",request.user.profile,'main')					

		elif project.stage=="estimate":
			project.stage="deployment"
			stages.append("deployment")
			project.stageHistory=stages
			filteredSurvey=project.survey.filter(stage="estimate", stageStatus="next", version="main").prefetch_related('icon')
			for x in filteredSurvey:
				DuplicateSurvey(x, "deployment","next",request.user.profile,'main')

		elif project.stage=="deployment":
			project.stage="as built"
			stages.append("as built")
			project.stageHistory=stages
			filteredSurvey=project.survey.filter(stage="deployment", stageStatus="next", version="main").prefetch_related('icon')
			for x in filteredSurvey:
				DuplicateSurvey(x, "as built","next",request.user.profile,'main')				

	#Keep the surveys from previous stage so it don't duplicate to next stage
	elif typpe=="previous":
		if project.stage=="survey":
			project.stage="profile"
			stages.append("profile")
			project.stageHistory=stages
			for x in project.survey.filter(stage="profile"):
				x.stageStatus="previous"
				x.save()

		elif project.stage=="design":
			project.stage="survey"
			stages.append("survey")
			project.stageHistory=stages
			for x in project.survey.filter(stage="survey"):
				x.stageStatus="previous"
				x.save()

		elif project.stage=="estimate":
			project.stage="design"
			stages.append("design")
			project.stageHistory=stages
			for x in project.survey.filter(stage="design"):
				x.stageStatus="previous"
				x.save()

	project.stageStatus=typpe
	project.save()
	serializer=ProjectDetailSerializer(project, many=False)
	return Response(serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def EditAddress(request):
	data=request.data.get("data")
	projectID=request.data.get("projectID")
	proj=Project.objects.get(id=int(projectID))
	proj.address=str(data)
	proj.save()
	return Response(status=HTTP_200_OK)

@api_view(["POST"])
def EditContact(request):
	data=json.loads(request.data.get("data"))
	projectID=request.data.get("projectID")
	proj=Project.objects.get(id=int(projectID))
	proj.firstName=data['firstName']
	proj.lastName=data['lastName']
	proj.email=data['email']
	proj.phone=data['phone']
	proj.save()
	return Response(status=HTTP_200_OK)

@api_view(["POST"])
def UploadAttachment(request):
	data=request.data
	projId=data.get("projectID")
	del data["projectID"]
	project=Project.objects.get(id=projId)
	for k,v in data.items():
		Attachment.objects.create(file=v, project=project, name=k)		
	attachments=AttachmentSerializer(Attachment.objects.filter(project=project), many=True)
	return Response(attachments.data, status=HTTP_200_OK)

@api_view(['POST'])
def DeleteFile(request):
	data=request.data
	Attachment.objects.get(id=data['file']).delete()
	project=Project.objects.get(id=data['projectID'])
	attachments=AttachmentSerializer(Attachment.objects.filter(project=project), many=True)
	return Response(attachments.data, status=HTTP_200_OK)

@api_view(['POST'])
def DeleteProject(request):
	data=request.data
	project=Project.objects.get(id=data).delete()
	return Response( status=HTTP_200_OK)

@api_view(["POST"])
def EditAssigned(request):
	data=request.data['datta']
	project=Project.objects.get(id=request.data['projectID'])
	paraofille={}
	am=[]
	for x in data['accountManager']:
		profile=Profile.objects.get(id=x['id'])
		am.append(profile)
	project.accountManager.set(am, clear=True)

	surv=[]
	for x in data['surveyer']:
		profile=Profile.objects.get(id=x['id'])
		surv.append(profile)
	project.surveyer.set(surv, clear=True)

	desg=[]
	for x in data['designer']:
		profile=Profile.objects.get(id=x['id'])
		desg.append(profile)
	project.designer.set(desg, clear=True)

	prop=[]
	for x in data['proposal']:
		profile=Profile.objects.get(id=x['id'])
		prop.append(profile)
	project.proposal.set(prop, clear=True)

	techs=[]
	for x in data['technician']:
		profile=Profile.objects.get(id=x['id'])
		techs.append(profile)
	project.technician.set(techs, clear=True)
	project.save()
	return Response(status=HTTP_200_OK)

@api_view(["POST"])
def DownloadCsv(request):
	data=json.loads(request.data)
	typpe=data['typpe']
	survey=Survey.objects.get(id=data['surveyID'])
	icons=survey.icon.all()
	headder=[]
	for x in icons:
		if x.name not in headder:
			headder.append(x.name)

	output = io.BytesIO()
	workbook = Workbook(output, {'in_memory': True})
	
	#Write sheet
	for x in headder:
		worksheet = workbook.add_worksheet(x)
		worksheet.set_column('A:A', 20)
		worksheet.write(1, 1, "Images")
		
		bold = workbook.add_format({'bold': True})		
		icon=icons.filter(name=x)
		ColNum=0
		#Write Header
		worksheet.write(1, ColNum, "Id")
		worksheet.write(0, ColNum, x)
		if typpe=="element":
			header=ast.literal_eval(icon[0].answer)
			for x in header:
				ColNum=ColNum+1
				worksheet.write(1, ColNum, x['fieldName'])

		elif typpe=="survey":
			header=["Category","Location","Element Height","Element Location","Budget Labor Cost"]
			for k in header:
				ColNum=ColNum+1
				worksheet.write(1, ColNum, k)

		elif typpe=="installation":
			header=["Installation","Assigned","Installed On","Installed By","Technician Assigned","Estimated Installation Time","Tech Type Required","	Specific Installation Notes"]
			for k in header:
				ColNum=ColNum+1
				worksheet.write(1, ColNum, k)
		
		worksheet.write(1, ColNum+1, "Images")
		#End of write header
		print(typpe)
		if typpe=="element":
			#Write Row
			for RowCount, value in enumerate(icon):
				Colcount=0
				worksheet.write(RowCount+2, Colcount,str(value.name)+" #"+ str(value.order))
				aranswer=ast.literal_eval(value.answer)

				#Write Col
				for value2 in aranswer:
					Colcount=Colcount+1
					worksheet.write(RowCount+2, Colcount, value2['answer'])

				icon_images = value.iconPicture.all()
				for count, picture in enumerate(icon_images):
					Colcount += 1
					worksheet.write(RowCount+2, Colcount, request.build_absolute_uri(picture.picture.url))

		elif typpe=="survey":
			for RowCount, value in enumerate(icon):
				Colcount=0
				worksheet.write(RowCount+2, Colcount,str(value.name)+" #"+ str(value.order))

				try :
					aranswer=ast.literal_eval(value.surveyToolbar)
					print(aranswer)
				except:
					aranswer={"selectedRadio":"","location":"","height":"","ellocation":"","budget":""}

				for v in aranswer.values():
					Colcount=Colcount+1
					worksheet.write(RowCount+2, Colcount, v)

				icon_images = value.iconPicture.all()
				for count, picture in enumerate(icon_images):
					Colcount += 1
					worksheet.write(RowCount+2, Colcount, request.build_absolute_uri(picture.picture.url))
				

		elif typpe=="installation":
			for RowCount, value in enumerate(icon):
				Colcount=0
				worksheet.write(RowCount+2, Colcount,str(value.name)+" #"+ str(value.order))

				try :
					aranswer=ast.literal_eval(value.installationToolbar)
				except:
					aranswer={"installation":"","assigned":"","installedon":"","installedby":"","technicianassigned":"","estimated":"","techreq":"","specific":""}

				for v in aranswer.values():
					Colcount=Colcount+1
					worksheet.write(RowCount+2, Colcount, v)

				icon_images = value.iconPicture.all()
				for count, picture in enumerate(icon_images):
					Colcount += 1
					worksheet.write(RowCount+2, Colcount, request.build_absolute_uri(picture.picture.url))				

	workbook.close()
	output.seek(0)
	response = HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = 'attachment; filename=test.xlsx'
	return response

@api_view(["POST"])
def DeleteClient(request):
	print(request.data)
	clientOrg=ClientOrganization.objects.get(id=request.data)
	clientOrg.delete()
	return Response(status=HTTP_200_OK)

@api_view(['POST'])
@requirePermissionsViews("CompanyAdmin","SuperAdmin","AccountManager")
def AddProjectClient(request):
	data=request.data
	clientOrg=ClientOrganization.objects.get(id=data['clientId'])	

	#Checking ig the number is exist
	Projj=Project.objects.filter(number=int(data['number']))
	if len(Projj)>0:
		return Response("Project number exist, please select another number",status=HTTP_200_OK)

	proj=Project.objects.create(name=data['name'], number=data['number'], company=clientOrg.company)
	proj.clientOrg.add(clientOrg)
	proj.save()

	try:
		for x in data['client']:
			client=Profile.objects.get(id=x['id'])
			proj.client.add(client)
		proj.save()
	except:pass

	return Response("success",status=HTTP_200_OK)

@api_view(["POST"])
def EditClientOrg(request):
	data=request.data
	clientOrg=ClientOrganization.objects.get(id=data['id'])
	clientOrg.name=data['name']
	clientOrg.number=data['number']
	clientOrg.email=data['email']
	clientOrg.location=data['location']
	clientOrg.save()
	return Response(status=HTTP_200_OK)

@api_view(["POST"])
def LoadTicketList(request):
	profile=request.user.profile
	data=request.data
	if profile.isClient and not profile.isSuperAdmin:
		tickets=Ticket.objects.filter(client=profile)
	else:
		company=Organization.objects.get(id=int(data))
		tickets=Ticket.objects.filter(company=company)
	serializer=TicketListSerializer(tickets, many=True)

	return Response(serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def GetTicket(request):
	profile=request.user.profile
	data=request.data
	ticket=Ticket.objects.get(ticketID=data)
	chatFiles=ChatFile.objects.filter(ticketID=data)

	if settings.MAIN:
		url="https://main.wiseeyes.link"
	else:
		url="http://127.0.0.1:8000"

	pic_list=[]
	chat_files=[]
	for y in ticket.ticketPicture.all():
		pic_url=request.build_absolute_uri(y.picture.url)
		pic_list.append(pic_url)

	for y in chatFiles:
		file_url=request.build_absolute_uri(y.file.url)
		chat_files.append({'file':file_url, 'chatID':y.chatID})

	if ticket.audioInfo:
		audio_info=json.loads(ticket.audioInfo)
		audio_dummy={
			'blobURL':request.build_absolute_uri(ticket.audioFile.url),
			'startTime':audio_info['startTime'],
			'stopTime':audio_info['stopTime'],
			'options':audio_info['options']
		}
	else:
		audio_dummy=None

	availTechs=ticket.project.technician.all()
	tech_list=ProfileSerializer2(availTechs, many=True)
	seria=TicketSerializer(ticket, many=False)

	serialData=seria.data
	serialData['audio'] = audio_dummy
	serialData['pictures'] = pic_list
	serialData['chatFiles']=chat_files
	serialData['availableTech']=tech_list.data

	if ticket.icon:
		icons=ticket.icon.all()
		serializerIcons=IconSerializer(icons, many=True)
		serialData['iconsData']=serializerIcons.data
	if ticket.surveyID:
		survey=Survey.objects.get(id=int(ticket.surveyID))
		surveySerial={'surveyName':survey.name,'surveyID':survey.id}
		serialData['surveyData']=surveySerial

	return Response(serialData, status=HTTP_200_OK)

@api_view(["POST"])
def CloseTicket(request):
	data=request.data
	now=datetime.now()
	time=datetime.strftime(now, '%Y-%m-%d %I:%M %p')
	ticket=Ticket.objects.get(id=int(data))
	ticket.status="Closed"
	ticket.dateUpdated=time
	ticket.save()
	if ticket.icon:
		for x in ticket.icon.all():
			x.isReported=False
			x.save()

	return Response(status=HTTP_200_OK)

@api_view(["POST"])
def AssignTech(request):
	data=request.data
	ticket=Ticket.objects.get(ticketID=int(data['ticketID']))
	technician_ids = [tech['id'] for tech in data['techs']]
	now=datetime.now()
	time=datetime.strftime(now, '%Y-%m-%d %I:%M %p')
	techs=Profile.objects.filter(id__in=technician_ids)
	ticket.technician.clear()
	ticket.technician.set(techs)	
	ticket.dateUpdated=time
	ticket.save()
	return Response(status=HTTP_200_OK)

@api_view(["POST"])
def TicketSeen(request):
	data=request.data
	profile=request.user.profile
	company=Organization.objects.get(id=int(data))		
	if profile.isSuperAdmin or profile.isAccountManager or profile.isCompanyAdmin:
		tickets=Ticket.objects.filter(company=company, seenByAdmin=False)
		for x in tickets:
			x.seenByAdmin=True
			x.save()
	else:
		tickets=Ticket.objects.filter(client=profile, seenByClient=False)
		for x in tickets:
			x.seenByClient=True
			x.save()
	
	return Response(status=HTTP_200_OK)

@api_view(["POST"])
def SubmitReply(request):
	data=json.loads(request.data['data'])
	darata=request.data
	profile=request.user.profile
	ticket=Ticket.objects.get(ticketID=data['ticketID'])
	now=datetime.now()
	time=datetime.strftime(now, '%Y-%m-%d %I:%M %p')

	if profile.isSuperAdmin or profile.isAccountManager or profile.isCompanyAdmin: 
		role="admin"	
	elif profile.isClient:
		role="client"
	elif profile.isTechnician:
		role="technician"

	if data['pilihan']=="client":
		chat=ast.literal_eval(ticket.clientChat)
		chat.append({'chatID':data['chatID'], "senderName":data['senderName'], 'senderID':data['senderID'], "text":data['text'],"role":data['role'],"time":data['time']})
		ticket.clientChat=str(chat)
	elif data['pilihan']=="tech":
		chat=ast.literal_eval(ticket.internalChat)
		chat.append({'chatID':data['chatID'], "senderName":data['senderName'], 'senderID':data['senderID'], "text":data['text'],"role":data['role'],"time":data['time']})
		ticket.internalChat=str(chat)
	ticket.dateUpdated=time
	ticket.save()

	for k,v in darata.items():
		if "files" in k:
			ChatFile.objects.create(chatID=data['chatID'], ticketID=ticket.ticketID, file=v)

	return Response(status=HTTP_200_OK)

@api_view(["POST"])
def SendNewTicket(request):
	data=request.data
	profile=request.user.profile
	for k,v in data.items():
		if k=="data":
			varavi=json.loads(v)
			project=Project.objects.get(id=int(varavi['project']['id']))
			now = datetime.now()
			date_str = now.strftime("%Y%m%d")
			random_str = str(random.randint(100, 999))
			ticketID=date_str + random_str
			company=Organization.objects.get(id=int(varavi['organization']))

			time=datetime.strftime(now, '%Y-%m-%d %I:%M %p')
			ticket=Ticket.objects.create(dateUpdated=time, dateCreated=time,ticketID=ticketID, project=project, client=profile, company=company, clientOrg=profile.clientOrg, subject=varavi['subject'], details=varavi['details'], status="Pending Operator Response")
			if profile.isClient:
				ticket.seenByAdmin=False
			else:
				ticket.seenByClient=False
			ticket.save()	

		elif "picture" in k:
			TicketPicture.objects.create(ticket=ticket, picture=v)

		elif k=="audio":
			if v!="null":
				ticket.audioInfo=v
				ticket.save()
		elif k=="audioBlob":
			ticket.audioFile.delete()
			ticket.save()
			ticket.audioFile=v
			ticket.save()
		elif k=="iconID":
			iconsid=ast.literal_eval(v)
			icons=Icon.objects.filter(iconid__in=iconsid)
			for icon in icons:
				icon.ticket.add(ticket)
				icon.isReported=True
				icon.save()				
		elif k =="surveyID":
			ticket.surveyID=v
			ticket.save()

	managerEmail=[]
	for x in project.accountManager.all():
		managerEmail.append(x.email)

	if settings.MAIN:
		url="https://main.wiseeyes.link"
	else:
		url="http://127.0.0.1:5173"
	subject=project.name+" #"+str(project.number)
	content="Ticket #"+ticket.ticketID+" has been created at project "+project.name+".<br/> Please check the ticket on this link : "+url+"/ticket/"+ticket.ticketID
	email = EmailMessage(subject, content, to=managerEmail)             
	email.content_subtype = "html" 

	try:
		pictures=ticket.ticketPicture.all()
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
		audio=ticket.audioFile
		email.attach(audio.name, audio.file.read(), "audio/mpeg")
	except: pass	
	email.send()
	return Response(status=HTTP_200_OK)

@api_view(["POST"])
def LiveBuiltsFetch(request):
	data = request.data
	profile = request.user.profile
	company = get_object_or_404(Organization.objects.prefetch_related("profile_set"), id=data)
	projects = Project.objects.prefetch_related("clientOrg").filter(company=company, client=profile, stage="as built")
	tickets=Ticket.objects.filter(company=company, seenByClient=False, client=profile)
	project_ids = [project.id for project in projects]
	surveys=Survey.objects.filter(project__id__in=project_ids, stage="as built")
	serializer_surveys=SurveySerializer(surveys, many=True)
	serializer_company = CompanySerializer(company)

	res={
		'unseenTicket':len(tickets),
		'surveys':serializer_surveys.data,		
		'organization': serializer_company.data,
	}
	return Response(res, status=HTTP_200_OK)