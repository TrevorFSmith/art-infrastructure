from django.test import TestCase, LiveServerTestCase
from django.core.urlresolvers import reverse
from ai.factories import *
from ai.test_helpers import *
from django.db import IntegrityError
from selenium.common.exceptions import NoSuchElementException

from rest_framework import status
from rest_framework.test import APITestCase
import json

from lighting import models as lighting_models


class ProjectorPriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        admin_login(self)

    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('lighting_api:projectors'))
        self.assertEqual(response.status_code, 200)

    def test_get_collection_of_projectors(self):
        ProjectorFactory()
        ProjectorFactory()
        response = self.client.get(reverse('lighting_api:projectors'))

        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(response.status_code, 200)

        object_keys = ["id", "name", "pjlink_host", "pjlink_port", "pjlink_password"].sort()
        response_keys = json.loads(response.content)[0].keys().sort()
        self.assertEqual(object_keys, response_keys)


    def test_delete_projector(self):
        projector = ProjectorFactory()
        count = lighting_models.Projector.objects.count()
        response = self.client.delete(reverse('lighting_api:projectors'),
                                   {"id": projector.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(lighting_models.Projector.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': projector.pk})


    def test_delete_nonexisting_projector(self):
        response = self.client.delete(reverse('lighting_api:projectors'),
                                   {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_noexisting_projector(self):
        response = self.client.put(reverse('lighting_api:projectors'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_with_errors_for_privileged_user(self):
        projector1 = ProjectorFactory()
        response = self.client.put(reverse('lighting_api:projectors'), {"id": projector1.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {"details":{"pjlink_host":["This field is required."],"name":["This field is required."]}})


    def test_update_without_errors_for_privileged_user(self):
        projector = ProjectorFactory()
        response = self.client.put(reverse('lighting_api:projectors'), {
            "id": projector.pk, "pjlink_host": "localhost", "name": "Projy",
            "pjlink_port": 8888, "pjlink_password": "pass"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        projector = lighting_models.Projector.objects.get(pk=projector.pk)

        response = json.loads(response.content)

        self.assertEqual(response["name"], "Projy")
        self.assertEqual(response["pjlink_host"], "localhost")
        self.assertEqual(response["pjlink_port"], 8888)
        self.assertEqual(response["pjlink_password"], "pass")


class ProjectorUnpriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        nonadmin_login(self)

    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('lighting_api:projectors'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('lighting_api:projectors'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_collection_of_projectors(self):
        response = self.client.get(reverse('lighting_api:projectors'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_projector(self):
        projector = ProjectorFactory()
        response = self.client.delete(reverse('lighting_api:projectors'),
                                   {"id": projector.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_nonexisting_projector(self):
        response = self.client.delete(reverse('lighting_api:projectors'),
                                   {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_noexisting_projector(self):
        response = self.client.put(reverse('lighting_api:projectors'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_with_errors_for_unprivileged_user(self):
        projector1 = ProjectorFactory()
        response = self.client.put(reverse('lighting_api:projectors'), {"id": projector1.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_without_errors_for_unprivileged_user(self):
        projector1 = ProjectorFactory()
        response = self.client.put(reverse('lighting_api:projectors'),
                                   {"id": projector1.pk, "pjlink_host": "localhost", "name": "Projy1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})
