from django.shortcuts import render
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Organization, ClientOrganization
from User.models import Profile
from .serializers import CompanySerializer, ClientOrgSerializer
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_403_FORBIDDEN,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK,
	HTTP_401_UNAUTHORIZED
)
from User.permissions import requirePermissionsViews
from Console.models import Project
from User.serializers import ProfileSerializer


@api_view(['POST'])
@requirePermissionsViews("SuperAdmin")
def RegisterCompany(request):
	data=request.data
	users=data['users']
	org=Organization.objects.create(name=data['name'], email=data['email'], number=data['number'], location=data['location'])
	for x in users:
		profile=Profile.objects.get(id=x['id'])
		profile.company.add(org)
		profile.save()
	res={
		"type":"success",
		"message":"Organization created"
	}
	return JsonResponse(res)

@api_view(['POST'])
@requirePermissionsViews("SuperAdmin", "CompanyAdmin", "AccountManager")
def RegisterClientOrg(request):
	data=request.data
	users=data['users']
	org=Organization.objects.get(id=data["organization_id"])
	client_org=ClientOrganization.objects.create(name=data['name'], email=data['email'], number=str(data['number']), location=data['location'], company=org)
	for x in users:
		profile=Profile.objects.get(id=x['id'])
		profile.clientOrg=client_org
		profile.save()
	return Response("success", status=HTTP_200_OK)	

@api_view(['GET'])
def GetCompanies(request):
	profile=request.user.profile
	try:
		if profile.isSuperAdmin:
			companies=Organization.objects.all()
		else:
			companies=profile.company.all()
	except:
		companies=[]
		
	serializer=CompanySerializer(companies, many=True)
	return Response(serializer.data, status=HTTP_200_OK)

@api_view(['POST'])
def GetAvailProfiles(request):
	comp_id=request.data
	company=Organization.objects.get(id=int(comp_id))
	profiles=company.profile_set.all()
	serializer=ProfileSerializer(profiles, many=True)
	return Response(serializer.data, status=HTTP_200_OK)

@api_view(['GET'])
def GetClientOrganizations(request):
	profile=request.user.profile
	try:
		if profile.isSuperAdmin:
			client_org=ClientOrganization.objects.all()
		else:
			company_id=profile.clientOrg.id
			client_org=ClientOrganization.objects.filter(id=company_id)
	except:
		client_org=[]
		
	serializer=ClientOrgSerializer(client_org, many=True)
	return Response(serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
def LoadClientOrg(request):
	ids=request.data
	clientOrg=ClientOrganization.objects.get(id=ids)
	clientUsers=Profile.objects.filter(isClient=True, company=clientOrg.company)
	clientOrgSerializer=ClientOrgSerializer(clientOrg, many=False)
	clientUserSerializer=ProfileSerializer(clientUsers, many=True)

	res={
		"clientOrg":clientOrgSerializer.data,
		"clientUsers":clientUserSerializer.data
	}
	return Response(res, status=HTTP_200_OK)


@api_view(["POST"])
@requirePermissionsViews("SuperAdmin")
def EditCompany(request):
	data=request.data
	company=Organization.objects.filter(id=data['id'])
	oneCompany=Organization.objects.get(id=data['id'])
	profiles=data['profiles']
	del data['profiles']
	profile_list=[]
	for x in profiles:
		profile_list.append(x['id'])
		Profile.objects.get(id=x['id']).company.add(oneCompany)

	for x in oneCompany.profile_set.all():	
		if x.id not in profile_list:
			x.company.remove(oneCompany)
			x.save()
	comp=company.update(**data)	
	res={
		"type":"success",
		"message":"Company edited"
	}
	return Response(res, status=HTTP_200_OK)

@api_view(["POST"])
@requirePermissionsViews("SuperAdmin", "AccountManager", "CompanyAdmin")
def EditClientOrganization(request):
	data=request.data
	clientOrg=ClientOrganization.objects.filter(id=data['id'])
	oneClientOrg=ClientOrganization.objects.get(id=data['id'])
	profiles=data['profiles']
	del data['profiles']
	profile_list=[]

	projects=data['projects']
	del data['projects']
	project_list=[]

	#Updating projects on organization
	for x in projects:
		project_list.append(x['id'])
		project=Project.objects.get(id=x['id'])
		project.clientOrg.add(oneClientOrg)
		project.save()

	for x in oneClientOrg.project.all():	
		if x.id not in project_list:
			x.clientOrg.remove(oneClientOrg)
			x.save()

	#Updating Users on organization
	for x in profiles:
		profile_list.append(x['id'])
		profile=Profile.objects.get(id=x['id'])
		profile.clientOrg=oneClientOrg
		profile.save()

	for x in oneClientOrg.profile.all():	
		if x.id not in profile_list:
			x.clientOrg=None
			x.save()

	comp=clientOrg.update(**data)	
	res={
		"type":"success",
		"message":"Company edited"
	}
	return Response(res, status=HTTP_200_OK)

@api_view(["POST"])
def AssignClientUser(request):
	data=request.data
	profiles=data['clientUser']
	oneClientOrg=ClientOrganization.objects.get(id=data['clientID'])
	profile_list=[]
	
	#Updating Users on organization
	for x in profiles:
		profile_list.append(x['id'])
		profile=Profile.objects.get(id=x['id'])
		profile.clientOrg=oneClientOrg
		profile.save()

	for x in oneClientOrg.profile.all():	
		if x.id not in profile_list:
			x.clientOrg=None
			x.save()

	return Response("Success", status=HTTP_200_OK)