from rest_framework import serializers
from .models import Organization
from User.serializers import ProfileSerializer
from Console.serializers import ProjectSerializer

class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = ["id","name","email","number","location"]

class ClientOrgSerializer(serializers.ModelSerializer):
	profiles=ProfileSerializer(source="profile", many=True)
	projects=ProjectSerializer(source="project", many=True)

	class Meta:
		model = Organization
		fields = ["id","name","email","number","location","profiles", 'projects']
		depth=1

