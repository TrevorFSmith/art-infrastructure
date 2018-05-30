from django.test import TestCase, LiveServerTestCase
from django.core.urlresolvers import reverse
from ai.factories import *
from ai.test_helpers import *
from django.db import IntegrityError
from selenium.common.exceptions import NoSuchElementException

from rest_framework import status
from rest_framework.test import APITestCase
import json

from iboot import models as iboot_models


class IBootPriviligedEndpointTestCase(APITestCase):


    def setUp(self):
        admin_login(self)


    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('iboot_api:iboots'))
        self.assertEqual(response.status_code, 200)


    def test_get_collection_of_iboots(self):
        IBootFactory()
        IBootFactory()
        response = self.client.get(reverse('iboot_api:iboots'))
        response_content = json.loads(response.content)

        self.assertEqual(response_content['count'], 2)
        self.assertEqual(len(response_content['results']), 2)
        self.assertEqual(response.status_code, 200)

        all_keys = ["count", "next", "previous", "results"]
        object_keys = ["id", "name", "mac_address", "host", "port", "commands"]
        response_all_keys = response_content.keys()
        response_object_keys = response_content['results'][0].keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
        self.assertEqual(sorted(object_keys), sorted(response_object_keys))


    def test_delete_iboot(self):
        iboot = IBootFactory()
        count = iboot_models.IBootDevice.objects.count()
        response = self.client.delete(reverse('iboot_api:iboots'), {"id": iboot.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(iboot_models.IBootDevice.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': iboot.pk})


    def test_delete_nonexisting_iboot(self):
        response = self.client.delete(reverse('iboot_api:iboots'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_noexisting_iboot(self):
        response = self.client.put(reverse('iboot_api:iboots'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_with_errors_for_privileged_user(self):
        iboot = IBootFactory()
        response = self.client.put(reverse('iboot_api:iboots'), {"id": iboot.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {"details":{"mac_address":["This field is required."],
                                     "name":["This field is required."],
                                     "host":["This field is required."]}})


    def test_update_without_errors_for_privileged_user(self):
        iboot = IBootFactory()
        response = self.client.put(reverse('iboot_api:iboots'),
            {"id": iboot.pk, "name": "iBoot1", "mac_address": "00-0D-AD-01-94-6F", "host": "127.0.0.1", "port": 8008})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        iboot = iboot_models.IBootDevice.objects.get(pk=iboot.pk)

        response = json.loads(response.content)

        self.assertEqual(response["name"], "iBoot1")
        self.assertEqual(response["mac_address"], "00-0D-AD-01-94-6F")
        self.assertEqual(response["host"], "127.0.0.1")
        self.assertEqual(response["port"], 8008)


class IBootUnpriviligedEndpointTestCase(APITestCase):


    def setUp(self):
        nonadmin_login(self)


    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('iboot_api:iboots'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('iboot_api:iboots'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_get_collection_of_iboots(self):
        response = self.client.get(reverse('iboot_api:iboots'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_iboot(self):
        iboot = IBootFactory()
        response = self.client.delete(reverse('iboot_api:iboots'), {"id": iboot.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_nonexisting_iboot(self):
        response = self.client.delete(reverse('iboot_api:iboots'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_noexisting_iboot(self):
        response = self.client.put(reverse('iboot_api:iboots'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_with_errors_for_unprivileged_user(self):
        iboot = IBootFactory()
        response = self.client.put(reverse('iboot_api:iboots'), {"id": iboot.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_without_errors_for_unprivileged_user(self):
        iboot = IBootFactory()
        response = self.client.put(reverse('iboot_api:iboots'),
            {"id": iboot.pk, "name": "iBoot1", "mac_address": "00-0D-AD-01-94-6F", "host": "127.0.0.1", "port": 8008})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})