from rest_framework import serializers
from .models import Profile, FreeUser

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = '__all__'
		depth=1

class ProfileSerializer2(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = '__all__'

class FreeuserSerializer(serializers.ModelSerializer):
	class Meta:
		model=FreeUser
		fields='__all__'