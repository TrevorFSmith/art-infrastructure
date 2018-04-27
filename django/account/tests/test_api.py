import os
import datetime
import simplejson
from datetime import timedelta

from django.core import mail
from django.conf import settings
from django.utils import timezone
from django.core.files import File
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ai.test_utils import create_user
from ai.test_utils import ExtendedTestCase

class ShareAPITest(ExtendedTestCase):

    def setUp(self):
        self.user1, self.client1 = create_user(username='alice', password='1234', first_name='Alice', last_name='Smith', email='alice@example.com', is_staff=True)
        self.user2, self.client2 = create_user(username='bob', password='1234', first_name='Bob', last_name='Roberts', email='bob@example.com')

    def test_current_user(self):
        info1 = self.getJSON(reverse('account_api:current_user_api_0_1'), self.client)
        self.assertEqual({}, info1)

        info2 = self.getJSON(reverse('account_api:current_user_api_0_1'), self.client1)
        self.assertEqual('Alice', info2['first_name'])
        self.assertEqual('Smith', info2['last_name'])
        self.assertEqual('Alice Smith', info2['display_name'])
        self.assertEqual(True, info2['staff'])

        info3 = self.getJSON(reverse('account_api:current_user_api_0_1'), self.client2)
        self.assertEqual(False, info3['staff'])
