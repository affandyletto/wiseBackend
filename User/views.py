from django.shortcuts import render
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile, FreeUser
from .serializers import ProfileSerializer, FreeuserSerializer, ProfileSerializer2
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_403_FORBIDDEN,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK,
	HTTP_401_UNAUTHORIZED
)
from rest_framework.permissions import IsAuthenticated
from .permissions import requirePermissionsViews
from Organization.models import Organization, ClientOrganization
from Organization.serializers import CompanySerializer
import json
import random
import string
from django.core.mail import EmailMessage

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        profile=Profile.objects.get(User=user)

        token['username'] = user.username
        token['isSuperAdmin'] = profile.isSuperAdmin
        token['isCompanyAdmin']= profile.isCompanyAdmin
        token['isAccountManager']= profile.isAccountManager        
        token['isTechnician']= profile.isTechnician
        token['isSurveyor']= profile.isSurveyor
        token['isDesigner']= profile.isDesigner
        token['isProposal']= profile.isProposal
        token['isClient']= profile.isClient
        token['isFreeUser']= profile.isFreeUser
        token['first_name']= profile.first_name
        token['last_name']=profile.last_name
        
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@requirePermissionsViews("CompanyAdmin","SuperAdmin","AccountManager")
def RegisterUser(request):
	data=request.data
	res={}
	#If the username exist, throw an error
	try:
		users=User.objects.filter(username=data['username'])
		if users:
			res={
				"type":"error",
				"message":"Username already exists, please pick a different username or log in with existing account"
			}
			return JsonResponse(res)
	except:
		pass

	try:
		users=User.objects.filter(email=data['email'])
		if users:
			res={
				"type":"error",
				"message":"Email already exists, please pick a different email or log in with existing account"
			}
			return JsonResponse(res)
	except:
		pass
	user_creation=User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])

	#Checking if the user has client organization
	try:		
		clientOrgID=data['clientOrg']
		clientOrg=ClientOrganization.objects.get(id=int(clientOrgID))
		del data['clientOrg']
	except:
		clientOrg=None
	#Create a profile object base on dictionary
	del data['username']
	del data['password']
	del data['cpassword']
	compList=[]

	try:
		for x in data['company']:
			compList.append(x['id'])

		del data['company']
	except:pass

	profile_creation=Profile.objects.create(**data, User=user_creation)
	
	if clientOrg:
		profile_creation.company.add(clientOrg.company)
		profile_creation.clientOrg=clientOrg
		profile_creation.save()
	else:
		for x in compList:
			company=Organization.objects.get(id=x)
			profile_creation.company.add(company)
			profile_creation.save()

	res={
		"type":"success",
		"message":"User created"
	}
	return JsonResponse(res)

@api_view(['POST'])
@requirePermissionsViews("CompanyAdmin","SuperAdmin","AccountManager")
def EditUser(request):
	data=request.data
	profile=Profile.objects.filter(id=data['id'])
	profOne=Profile.objects.get(id=data['id'])
	try:
		del data['history']
	except:pass
	del data['User']

	comp_list=[]
	for x in data['company']:
		comp_list.append(x['id'])
	companies=Organization.objects.filter(id__in=comp_list)
	try:
		del data['company']	
		del data['clientOrg']
		prof=profile.update(**data)		
		profOne.company.set(companies)
		profOne.save()
		prof.save()
	except:
		prof=profile.update(**data)
		try:
			prof.save()
		except:
			pass

	res={
		"type":"success",
		"message":"User edited"
	}
	return JsonResponse(res)

@api_view(['POST'])
@requirePermissionsViews("SuperAdmin","CompanyAdmin","AccountManager")
def GetProfiles(request):
	profile=request.user.profile
	#request value = 0 means showing all organization
	if request.data==0:
		company=Organization.objects.all()
		profiles=Profile.objects.select_related('User').all()
	elif profile.isAccountManager and not profile.isCompanyAdmin:
		company=Organization.objects.get(id=request.data)
		profiles=Profile.objects.select_related('User').filter(company=company).exclude(isCompanyAdmin=True)
	else:
		company=Organization.objects.get(id=request.data)
		profiles=Profile.objects.select_related('User').filter(company=company)

	serializerProfile=ProfileSerializer(profiles, many=True)

	if profile.isSuperAdmin or request.data==0:
		companies=Organization.objects.all()
	else:
		companies=profile.company.all()
		
	serializerCompany=CompanySerializer(companies, many=True)
	resData={
		'profiles':serializerProfile.data,
		'companies':serializerCompany.data
	}
	return JsonResponse(resData)

@api_view(['POST'])
@requirePermissionsViews("CompanyAdmin","SuperAdmin","AccountManager")
def ModifyRoles(request):
	profile_id=request.data['id']
	history=request.data['history']
	profile=Profile.objects.select_related('User').filter(id=profile_id)

	for x in history:
		if "isCompanyAdmin" in x or "isAccountManager" in x:
			profile.update(**x,isPrevilageChange=True)
		else:
			profile.update(**x)
	res={
		"type":"success",
		"message":"User role modified"
	}
	return JsonResponse(res)

@api_view(['POST'])
@requirePermissionsViews("CompanyAdmin","SuperAdmin","AccountManager")
def DeleteUser(request):
	profile_id=request.data['id']
	user=Profile.objects.select_related('User').get(id=profile_id).User.delete()
	res={
		"type":"success",
		"message":"User deleted"
	}
	return JsonResponse(res)

@api_view(["POST"])
def FreeSubmit(request):
	inputData=json.loads(request.data.get('inputData'))
	file=request.data.get('file')
	username=inputData['username']
	try:
		user=User.objects.get(username=username)
		return Response("errorUsername")
	except:
		pass

	FreeUser.objects.create(**inputData, file=file)

	return Response(HTTP_200_OK)

@api_view(["GET"])
def GetFreeUser(request):
	freeUsers=FreeUser.objects.all()
	serializer=FreeuserSerializer(freeUsers, many=True)
	return Response(serializer.data, HTTP_200_OK)

@api_view(["POST"])
def GetMyInfo(request):
	myProfile=ProfileSerializer2(request.user.profile, many=False)
	return Response(myProfile.data, HTTP_200_OK)

@api_view(["POST"])
def FreeApprove(request):
	user=request.data

	for i in range(3):
	    result_str = ''.join(random.sample(string.ascii_lowercase, 8))

	org=Organization.objects.create(name=user['company_name'], email=user['work_email'], number=user['work_number'], location=user['work_address'])
	user_creation=User.objects.create_user(username=user['username'], email=user['email'], password=result_str)
	profile=Profile.objects.create(first_name=user['first_name'], last_name=user['last_name'], email=user['email'], phone_number=user['phone_number'], User=user_creation, isFreeUser=True)
	profile.company.add(org)
	profile.save()
	fu=FreeUser.objects.get(id=user['id'])
	fu.approved=True
	fu.save()

	first_name=user['first_name']
	username=user['username']
	password=result_str
	content=[]
	content.append("<html>Hello "+first_name+",")
	content.append("We have approved your request to try out WiseEyes. Please visit {wiseeyes website} to begin using our product. Your username: "+username+", and password: "+password+". Please note that this application is currently in development and updating on a daily basis, so there might be minor issues that we are working on solving. If you have any suggestions or concerns feel free to email us at wiseeyes@innovaaccelerator.com.<br/>")
	content.append("In addition please feel free to look at <a href='https://www.asoneforce.com/'>https://www.asoneforce.com/</a> and consider joining our team. We are a strategic partnership program that helps to increase your revenue, get more local projects, scale up, Beat Your Competition and Say Yes to More Opportunities! <br/>")
	content.append("WiseEyes Development Team</html>")
	joinedContent="<br/>".join(content)
	email = EmailMessage("Wise eyes free user", joinedContent ,to=[user['email']])             
	email.content_subtype = "html" 
	email.send()

	return Response(HTTP_200_OK)

