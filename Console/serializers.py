from rest_framework import serializers
from .models import Project, Attachment, Ticket
from User.serializers import ProfileSerializer
from Survey.serializers import SurveySerializer
from datetime import datetime
import ast

class TicketSerializer(serializers.ModelSerializer):	
	internalChat=serializers.SerializerMethodField()
	clientChat=serializers.SerializerMethodField()
	class Meta:
		model=Ticket
		fields="__all__"
		depth=1

	def get_internalChat(self, obj):
		qwe=ast.literal_eval(obj.internalChat)
		return qwe

	def get_clientChat(self, obj):
		qwe=ast.literal_eval(obj.clientChat)
		return qwe

class TicketListSerializer(serializers.ModelSerializer):
	projectName = serializers.CharField(source='project.name', read_only=True)

	class Meta:
		model = Ticket
		fields = ['ticketID', 'subject', 'status', 'projectName', 'dateUpdated','seenByClient', 'seenByAdmin']

class AttachmentSerializer(serializers.ModelSerializer):
	class Meta:
		model=Attachment
		fields=["project", 'file','name', 'id']

class ProjectSerializer(serializers.ModelSerializer):
	surveyIDS=serializers.SerializerMethodField()
	surveyAvail=serializers.SerializerMethodField()
	class Meta:
		model = Project
		fields = ["id","name","number",'surveyIDS','surveyAvail',"clientOrg", 'stage',"client",'firstName','lastName','phone']
		depth=1

	def get_surveyIDS(self, obj):
		qwe=[]
		for x in obj.survey.all():
			if x.stage=="as built":
				qwe.append({'id':x.id, 'name':x.name})
		return qwe

	def get_surveyAvail(self, obj):
		qwe=[]
		for x in obj.survey.all():
			if x.version=="main" and x.stage!="as built" and x.stage==obj.stage:
				qwe.append({'id':x.id, 'name':x.name, 'stage':x.stage, 'projName':obj.name})
		return qwe

class ProjectDetailSerializer(serializers.ModelSerializer):
	accountManager=ProfileSerializer(many=True)
	surveyer=ProfileSerializer(many=True)
	designer=ProfileSerializer(many=True)
	proposal=ProfileSerializer(many=True)
	technician=ProfileSerializer(many=True)
	survey=SurveySerializer(many=True)
	attachment=AttachmentSerializer( many=True)
	class Meta:
		model=Project
		fields=["id","name","company",
		"nickname","number",'clientOrg','stage',"subCategory",
		"accountManager","surveyer",'designer','proposal',
		'technician','firstName','lastName','email',
		'phone', 'survey',
		'startDate','endDate','hibernate', 'address', 'attachment'
		]
		depth=1