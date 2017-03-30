from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

def user_display_name(user):
	if user.get_full_name(): return user.get_full_name()
	return user.username

def user_staff(user): return user.is_staff

User.display_name = property(user_display_name)
User.staff = property(user_staff)
