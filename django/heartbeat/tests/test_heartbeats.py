import os
import urllib
from datetime import timedelta

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django.core.files import File
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ai.test_utils import (
	create_user,
	ExtendedTestCase
)

from artwork.models import (
	Installation
)

from heartbeat.models import (
	Heartbeat
)

from heartbeat.views import (
	INFO_PARAMETER,
	INSTALLATION_ID_PARAMETER,
	CLEAN_HEARTBEATS_PARAMETER
)

class HeartbeatsTest(ExtendedTestCase):

	def setUp(self):
		self.user1, self.client1 = create_user(username='alice', password='1234', first_name='Alice', last_name='Flowers', email='alice@example.com')
		self.user2, self.client2 = create_user(username='bob', password='1234', first_name='Bob', last_name='Roberts', email='bob@example.com')
		self.user3, self.client3 = create_user(username='tiger', password='1234', first_name='Tiger', last_name='Regit', email='tiger@example.com')

	def test_api(self):
		response = self.client.get(reverse('heartbeat:index'))
		self.assertEqual(response.status_code, 200) # anonymous access should be possible
		self.assertEqual(Heartbeat.objects.all().count(), 0)

		response = self.client.get(reverse('heartbeat:index') + urllib.urlencode({
			INSTALLATION_ID_PARAMETER: 11234567,
			INFO_PARAMETER: 'info'
		}))
		self.assertEqual(response.status_code, 404) # Unknown id
		self.assertEqual(Heartbeat.objects.all().count(), 0) # bogus installation ID

		installation1 = Installation.objects.create(name='Installation 1')
		installation_url = reverse('heartbeat:index') + '?' + urllib.urlencode({
			INSTALLATION_ID_PARAMETER: installation1.id,
			INFO_PARAMETER: 'info'
		})

		response = self.client.get(installation_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Heartbeat.objects.all().count(), 1)
		heartbeat1 = Heartbeat.objects.all().first()
		self.assertEqual(heartbeat1.installation, installation1)

		response = self.client.get(installation_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Heartbeat.objects.all().count(), 2)
		heartbeat2 = Heartbeat.objects.all().first()
		self.assertEqual(heartbeat2.installation, installation1)
