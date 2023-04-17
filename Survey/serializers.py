from rest_framework import serializers
from .models import Survey, Category, IconBase, Icon, Cable, SavedSurvey
from django.conf import settings

class SurveySerializer(serializers.ModelSerializer):
	surveyPicture = serializers.SerializerMethodField()
	picture = serializers.SerializerMethodField()

	class Meta:
		model=Survey
		fields="__all__"
		depth=1

	def get_surveyPicture(self, obj):
		if settings.MAIN:
			url="https://main.wiseeyes.link"
		else:
			url="http://127.0.0.1:8000"		

		if(obj.surveyPicture):
			return url+obj.surveyPicture.url
		else:
			return url+obj.picture.url

	def get_picture(self, obj):
		if settings.MAIN:
			url="https://main.wiseeyes.link"
		else:
			url="http://127.0.0.1:8000"
		return url+obj.picture.url

class SavedSurveySerializer(serializers.ModelSerializer):
	person_name = serializers.SerializerMethodField()
	stage = serializers.SerializerMethodField()
	version = serializers.SerializerMethodField()
	class Meta:
		model=SavedSurvey
		fields="__all__"

	def get_person_name(self, obj):
		if obj.editedProfile:
			return obj.editedProfile.first_name+" "+obj.editedProfile.last_name
		else:
			return ""

	def get_stage(self, obj):
		return obj.survey.stage

	def get_version(self, obj):
		return obj.survey.version

class IconSerializer(serializers.ModelSerializer):
	image=serializers.SerializerMethodField()

	class Meta:
		model=Icon
		fields=['iconid','name','order','angle',"depth","opacity","color","rotate","xposition","yposition","isLocked","isReported","unit",'answer', 'image', 'dateUpdated', 'startDate', 'endDate', 'techName', 'test', 'comment']

	def get_image(self, obj):
		if settings.MAIN:
			url="https://main.wiseeyes.link"
		else:
			url="http://127.0.0.1:8000"
		return url+obj.thumbnail.url

class CableSerializer(serializers.ModelSerializer):
	image=serializers.SerializerMethodField()

	class Meta:
		model=Cable
		fields=['iconid','name','order',"depth","color","line","isLocked","isReported","unit",'answer', 'image', 'dateUpdated', 'startDate', 'endDate', 'techName', 'test', 'comment']

	def get_image(self, obj):
		if settings.MAIN:
			url="https://main.wiseeyes.link"
		else:
			url="http://127.0.0.1:8000"
		return url+obj.thumbnail.url

class IconBaseSerializer(serializers.ModelSerializer):
	thumbnail=serializers.SerializerMethodField()
	class Meta:
		model=IconBase
		fields=["id","name","thumbnail","field", "category", "project"]

	def get_thumbnail(self, obj):
		if settings.MAIN:
			url="https://main.wiseeyes.link"
		else:
			url="http://127.0.0.1:8000"
		return url+obj.thumbnail.url

class CategorySerializer(serializers.ModelSerializer):
	iconBase=IconBaseSerializer(many=True)
	thumbnail=serializers.SerializerMethodField()
	class Meta:
		model=Category
		fields=["id","name","thumbnail","iconBase","priority"]
		depth=1

	def get_thumbnail(self, obj):
		if settings.MAIN:
			url="https://main.wiseeyes.link"
		else:
			url="http://127.0.0.1:8000"
		try:
			return url+obj.thumbnail.url
		except:
			return ""