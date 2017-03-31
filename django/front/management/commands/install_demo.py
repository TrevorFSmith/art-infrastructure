import os
import csv
import sys
import time
import urllib
import random
from PIL import Image
from datetime import date, timedelta

from django.conf import settings
from django.db import connection
from django.utils import encoding
from django.utils import timezone
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from rest_framework.authtoken.models import Token

from artwork.models import (
	Artist,
	ArtistGroup,
	Photo,
	EquipmentType,
	Equipment,
	Document,
	InstallationSite,
	Installation
)

from heartbeat.models import (
	Heartbeat
)

class Command(BaseCommand):
	help = "Installs the demo data."
	requires_system_checks = True

	def handle(self, *labels, **options):
		if settings.PRODUCTION:
			print 'I will not install the demo on a PRODUCTION machine.  Sorry.'
			return

		call_command('migrate', interactive=False)

		Photo.objects.all().delete()
		Document.objects.all().delete()
		ArtistGroup.objects.all().delete()
		Artist.objects.all().delete()
		Equipment.objects.all().delete()
		EquipmentType.objects.all().delete()
		Installation.objects.all().delete()
		InstallationSite.objects.all().delete()
		Heartbeat.objects.all().delete()
		User.objects.all().delete()
		Token.objects.all().delete()

		site = Site.objects.get_current()
		site.domain = '127.0.0.1:8000'
		site.name = 'Art Infrastructure'
		site.save()

		self.create_user('trevor', '1234', 'trevor@example.com', 'Trevor F.', 'Smith', True, True)
		self.create_user('matt', '1234', 'matt@example.com', 'Matt', 'Gorbet', True, True)

		artist1 = Artist.objects.create(name='Anthony Jones', email='aj@example.com', phone='206-555-1212', url='http://example.com/')
		artist2 = Artist.objects.create(name='Davone Smith', email='ds@example.com', phone='206-555-1212', url='http://example.com/')
		artist_group1 = ArtistGroup.objects.create(name='Light Strip Collective', url='http://example.com/')
		artist_group1.artists.add(artist1, artist2)

		artist3 = Artist.objects.create(name='Wendy Doe', email='wd@example.com', phone='206-555-1212', url='http://example.com/')
		artist4 = Artist.objects.create(name='Jasmin Hense', email='jh@example.com', phone='206-555-1212', url='http://example.com/')
		artist5 = Artist.objects.create(name='Steph Able', email='sa@example.com', phone='206-555-1212', url='http://example.com/')
		artist_group2 = ArtistGroup.objects.create(name='Four Kinds of Earth', url='http://example.com/')
		artist_group2.artists.add(artist3, artist4, artist5)

		artist6 = Artist.objects.create(name='Moon Unit Alpha', email='mua@example.com', phone='206-555-1212', url='http://example.com/')

		installation_site1 = InstallationSite.objects.create(name='Baggage Claim', location='South Terminal')
		installation_site2 = InstallationSite.objects.create(name='Concourse Wall', location='South Terminal')
		installation_site3 = InstallationSite.objects.create(name='Large Showcase 1', location='South Terminal')
		installation_site4 = InstallationSite.objects.create(name='Large Showcase 2', location='South Terminal')

		installation1 = Installation.objects.create(name='Curio Cabinet 1', site=installation_site3, opened=timezone.now() - timedelta(days=60))
		installation1.artists.add(artist6)

		installation2 = Installation.objects.create(name='Bags from Heaven', site=installation_site1, opened=timezone.now() - timedelta(days=120), closed=timezone.now() - timedelta(days=10))
		installation2.groups.add(artist_group1)

		installation3 = Installation.objects.create(name='Apple of my Eye', site=installation_site1, opened=timezone.now() - timedelta(days=10))
		installation3.groups.add(artist_group2)

	def create_user(self, username, password, email, first_name=None, last_name=None, is_staff=False, is_superuser=False):
		user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, is_staff=is_staff, is_superuser=is_superuser)
		user.set_password(password)
		user.save()

		return user

