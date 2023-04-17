from django.shortcuts import render
from Survey.models import Survey
import json
import ast
import random
import string
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_403_FORBIDDEN,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK,
	HTTP_401_UNAUTHORIZED
)
from User.permissions import requirePermissionsViews
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Proposal, Section, Page, Element
from .serializers import ProposalSerializer
from django.core.mail import EmailMessage
from django.conf import settings
from PIL import Image
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from django.core.files.storage import default_storage

def generate_random_string_and_number():
    # Generate a random string of length 8
    random_string = ''.join(random.choices(string.ascii_letters, k=18))
    # Generate a random number between 1 and 100
    random_number = random.randint(1, 10000)
    # Convert number to string
    random_number = str(random_number)
    # Randomly insert the number into the string
    pos = random.randint(0, len(random_string))
    random_string = random_string[:pos] + random_number + random_string[pos:]
    return random_string

def pictures_to_pdf(pictures):
    buffer = BytesIO()
    (w, h) = letter
    c = canvas.Canvas(buffer, pagesize=letter)
    for picture in pictures:
        img = Image.open(picture)
        img.load()
        img_reader = ImageReader(img)
        c.drawImage(img_reader, 0, 0, w, h)
        c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

@api_view(["POST"])
def AddProposal(request):
	data=request.data
	name=data['name']
	proposalid=data['proposalid']		
	if data['type']=="surveyProposal":
		survey=Survey.objects.get(id=data['surveyid'])
	else:
		survey=None
	proposal=Proposal.objects.create(name=name, proposalid=proposalid, typpe=data['type'], survey=survey)
	
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def AddSection(request):
	name=request.data['name']
	sectionid=request.data['sectionid']
	proposalid=request.data['proposalid']
	no=request.data['no']
	proposal=Proposal.objects.get(proposalid=proposalid)
	Section.objects.create(sectionid=sectionid, name=name, proposal=proposal, no=no)
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def AddPage(request):
	data=request.data
	section=Section.objects.get(sectionid=data['sectionid'])
	Page.objects.create(section=section, proposal=section.proposal, pageid=data['pageid'],no=data['no'], color=data['color'], bgUrl=data['bgUrl'])
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def AddElement(request):
	data=json.loads(request.data['data'])
	page=Page.objects.get(pageid=data['pageid'])
	if data['type']=="textBox":
		Element.objects.create(elementid=data['elementid'], typpe="textBox", page=page,section=page.section,proposal=page.section.proposal, loc=str(data['loc']))
	elif data['type']=="image":
		try:
			immage=request.data['img']
		except:
			immage=data['imgUrl']
		Element.objects.create(image=immage, elementid=data['elementid'], typpe="image", page=page,section=page.section,proposal=page.section.proposal, loc=str(data['loc']), imgSize=str(data['imgSize']), configuration=str(data['configuration']))
	elif data['type']=="signArea":

		try:
			immage=request.data['img']
		except:
			immage=data['imgUrl']
		Element.objects.create(image=immage, elementid=data['elementid'], typpe="signArea", page=page,section=page.section,proposal=page.section.proposal, loc=str(data['loc']), imgSize=str(data['imgSize']), configuration=str(data['configuration']))
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def GetProposals(request):
	proposals=Proposal.objects.all().exclude(typpe="signProposal")
	res=[]
	for x in proposals:
		if x.thumbnail:
			proposal={'name':x.name,'proposalid':x.proposalid,'thumbnail':request.build_absolute_uri(x.thumbnail.url)}
			res.append(proposal)		

	return Response(res, status=HTTP_200_OK)

@api_view(["POST"])
def SaveThumbnail(request):
	data=request.data
	proposal=Proposal.objects.get(proposalid=data['proposalid'])
	proposal.thumbnail.delete()
	proposal.save()
	proposal.thumbnail=data['proposal_thumbnail']
	proposal.save()
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def SendSignedProposal(request):
	data=request.data
	images=[]
	for k,v in data.items():
		if k=="proposalid":
			proposal=Proposal.objects.get(proposalid=int(v))
		if k!="proposalid":
			images.insert(0,v)
	pdf=pictures_to_pdf(images)
	email = EmailMessage("Approved ", to=[proposal.senderEmail])             
	email.content_subtype = "html" 
	email.attach("pdf", pdf, "application/pdf")
	email.send()
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def SendSign(request):
	data=request.data
	proposal=Proposal.objects.get(proposalid=data['proposal']['id'])
	proposId=random.randint(1, 1000000000)
	proposCode=generate_random_string_and_number()
	new_proposal = Proposal.objects.create(
		name=f"Copy of {proposal.name}",
		typpe="signProposal",
		proposalid=proposId,
		thumbnail=proposal.thumbnail,
		proposCode=proposCode,
		survey=proposal.survey,
		senderEmail=request.user.profile.email,
	)
	url=""
	if settings.MAIN:
		url="https://rocket.onesurveyapp.com/signProposal/"+proposCode
	else:
		url="http://localhost:3000/signProposal/"+proposCode

	# add the company to the new proposal
	new_proposal.company.set(proposal.company.all())

	# duplicate sections
	for section in proposal.section.all():
		new_section = Section.objects.create(
			no=section.no,
			sectionid=random.randint(1, 1000000000),
			name=section.name,
			proposal=new_proposal
		)
		# duplicate pages
		for page in section.page.all():
			new_page = Page.objects.create(
				no=page.no,
				pageid=random.randint(1, 1000000000),
				color=page.color,
				bgUrl=page.bgUrl,
				proposal=new_proposal,
				section=new_section
			)
			# duplicate elements
			for element in page.element.all():
				Element.objects.create(
					elementid=random.randint(1, 1000000000),
					typpe=element.typpe,
					loc=element.loc,
					configuration=element.configuration,
					image=element.image,
					text=element.text,
					imgSize=element.imgSize,
					imgUrl=element.imgUrl,
					size=element.size,
					transform=element.transform,
					section=new_section,
					proposal=new_proposal,
					page=new_page
				)

	email = EmailMessage("Proposal need to sign", "Please click on this link : "+url, to=[data['email']])             
	email.content_subtype = "html" 
	email.send()
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def EditElement(request):
	data=request.data['data']
	typpe=request.data['type']
	element=Element.objects.get(elementid=data['id'])
	if typpe=="resizeImage":
		element.imgSize=data['imgSize']
	elif typpe=="resizeBox":
		element.size=data['size']
	elif typpe=="stopDrag":
		element.configuration=data['configuration']
		element.transform=data['transform']
	elif typpe=="editText":
		element.text=data['text']
	element.save()

	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def FetchProposal(request):
	data=request.data
	if data['typpe']=="signProposal":
		proposal=Proposal.objects.get(proposCode=str(data['proposalid']))
	else:
		proposal=Proposal.objects.get(proposalid=int(data['proposalid']))
	sections=[]
	elements=[]
	for x in proposal.section.all():
		pages=[]
		for y in x.page.all():
			if y.bgImage:
				if settings.MAIN:
					url="https://main.wiseeyes.link"
				else:
					url="http://127.0.0.1:8000"
				bgUrl=url+y.bgImage.url
			else:
				bgUrl=""
			page={'no':y.no, 'id':y.pageid, 'color':y.color, 'bgUrl':bgUrl}
			pages.append(page)
		section={"pages":pages, 'id':x.sectionid, "name":x.name, "no":x.no }
		sections.append(section)

	for x in proposal.element.all():
		if x.image:
			immage=request.build_absolute_uri(x.image.url)
			imgSize=ast.literal_eval(x.imgSize)
		else:
			immage=None
			imgSize=None

		if x.configuration:
			configuration=ast.literal_eval(x.configuration)
		else:
			configuration=None

		if x.size:
			size=ast.literal_eval(x.size)
		else:
			size=None

		page={"id":x.page.pageid}
		element={'id':x.elementid, 'type':x.typpe, 'loc':ast.literal_eval(x.loc), 'transform':x.transform,
		'configuration':configuration, 'imgUrl':immage, 'imgSize':imgSize, "page":page, "text":x.text, "size":size}
		elements.append(element)

	res={
		'sections':sections,
		'elements':elements,
		'proposal':{'id':proposal.proposalid,"typpe":proposal.typpe, 'name':proposal.name, "thumbnail":request.build_absolute_uri(proposal.thumbnail.url) if proposal.thumbnail else ""}
	}
	return Response(res, status=HTTP_200_OK)

@api_view(["POST"])
def DeleteElement(request):
	data=request.data
	element=Element.objects.get(elementid=int(data))
	element.delete()
	return Response("Success", status=HTTP_200_OK)

@api_view(['POST'])
def HandleDelete(request):
	data=request.data
	ids=data['id']
	typpe=data['type']
	if typpe=="page":
		page=Page.objects.get(pageid=ids)
		page.delete()
	elif typpe=="element":
		element=Element.objects.get(elementid=ids)
		element.delete()
	elif typpe=="section":
		section=Section.objects.get(sectionid=ids)
		section.delete()
	return Response("Success", status=HTTP_200_OK)

@api_view(["POST"])
def ChangePageBackground(request):
	data=request.data
	page=Page.objects.get(pageid=data['pageid'])
	if data['type']=="color":
		page.color=data['color']
	elif data['type']=="image":
		page.bgImage=data['image']

	page.save()
	return Response("Success", status=HTTP_200_OK)
