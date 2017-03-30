from rest_framework import serializers

from django.contrib.auth.models import User

class PublicUserSerializer_0_1(serializers.HyperlinkedModelSerializer):
	"""
	User info shown to any user, for example during user searches.
	"""
	class Meta:
		model = User
		fields = ('id', 'username', 'staff', 'date_joined', 'first_name', 'last_name', 'display_name')

class SelfUserSerializer_0_1(serializers.HyperlinkedModelSerializer):
	"""
	Shown only to the users who data this is because it includes fields like email
	"""
	class Meta:
		model = User
		fields = ('id', 'username', 'staff', 'date_joined', 'first_name', 'last_name', 'display_name', 'email')
