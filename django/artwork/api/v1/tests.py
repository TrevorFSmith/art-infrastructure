from django.test import TestCase, LiveServerTestCase
from django.core.urlresolvers import reverse
from ai.factories import *
from ai.test_helpers import *
from django.db import IntegrityError
from selenium.common.exceptions import NoSuchElementException

from rest_framework import status
from rest_framework.test import APITestCase
import json

from artwork import models as artwork_models


class ArtistPriviligedEndpointTestCase(APITestCase):


    def setUp(self):
        admin_login(self)


    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('artwork_api:artists'))
        self.assertEqual(response.status_code, 200)


    def test_get_collection_of_artists(self):
        ArtistFactory()
        ArtistFactory()
        response = self.client.get(reverse('artwork_api:artists'))
        response_content = json.loads(response.content)

        self.assertEqual(response_content['count'], 2)
        self.assertEqual(len(response_content['results']), 2)
        self.assertEqual(response.status_code, 200)

        all_keys = ["count", "next", "previous", "results"]
        object_keys = ["id", "name", "email", "phone", "artistgroup_set", "groups_info", "url", "notes", "created"]
        response_all_keys = response_content.keys()
        response_object_keys = response_content['results'][0].keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
        self.assertEqual(sorted(object_keys), sorted(response_object_keys))


    def test_delete_artist(self):
        artist = ArtistFactory()
        count = artwork_models.Artist.objects.count()
        response = self.client.delete(reverse('artwork_api:artists'), {"id": artist.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(artwork_models.Artist.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': artist.pk})


    def test_delete_nonexisting_artist(self):
        response = self.client.delete(reverse('artwork_api:artists'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_noexisting_artist(self):
        response = self.client.put(reverse('artwork_api:artists'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_with_errors_for_privileged_user(self):
        artist = ArtistFactory()
        response = self.client.put(reverse('artwork_api:artists'), {"id": artist.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"details":{"name":["This field is required."],
                                                                   "artistgroup_set":["This field is required."]}})


    def test_update_without_errors_for_privileged_user(self):
        artist = ArtistFactory()
        response = self.client.put(reverse('artwork_api:artists'),
            {"id": artist.pk, "name": "Artist1", "email": "artist1.example.com", 
            "phone": "111-111-111", "notes": "Notes1", "artistgroup_set": []})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = json.loads(response.content)
        self.assertEqual(response["name"], "Artist1")
        self.assertEqual(response["email"], "artist1.example.com")
        self.assertEqual(response["phone"], "111-111-111")
        self.assertEqual(response["notes"], "Notes1")


class ArtistUnpriviligedEndpointTestCase(APITestCase):


    def setUp(self):
        nonadmin_login(self)


    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:artists'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:artists'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_get_collection_of_artists(self):
        response = self.client.get(reverse('artwork_api:artists'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_artist(self):
        artist = ArtistFactory()
        response = self.client.delete(reverse('artwork_api:artists'), {"id": artist.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_nonexisting_artist(self):
        response = self.client.delete(reverse('artwork_api:artists'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_noexisting_artist(self):
        response = self.client.put(reverse('artwork_api:artists'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_with_errors_for_unprivileged_user(self):
        artist = ArtistFactory()
        response = self.client.put(reverse('artwork_api:artists'), {"id": artist.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_without_errors_for_unprivileged_user(self):
        artist = ArtistFactory()
        response = self.client.put(reverse('artwork_api:artists'),
            {"id": artist.pk, "name": "Artist1", "email": "artist1.example.com", "phone": "111-111-111", "notes": "Notes1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


class ArtistGroupPriviligedEndpointTestCase(APITestCase):


    def setUp(self):
        admin_login(self)


    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('artwork_api:artist_groups'))
        self.assertEqual(response.status_code, 200)


    def test_get_collection_of_artist_groups(self):
        ArtistGroupFactory()
        ArtistGroupFactory()
        response = self.client.get(reverse('artwork_api:artist_groups'))
        response_content = json.loads(response.content)

        self.assertEqual(response_content['count'], 2)
        self.assertEqual(len(response_content['results']), 2)
        self.assertEqual(response.status_code, 200)

        all_keys = ["count", "next", "previous", "results"]
        object_keys = ["id", "name", "artists", "artists_info", "url", "created"]
        response_all_keys = response_content.keys()
        response_object_keys = response_content['results'][0].keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
        self.assertEqual(sorted(object_keys), sorted(response_object_keys))


    def test_delete_artist_group(self):
        artist_group = ArtistGroupFactory()
        count = artwork_models.ArtistGroup.objects.count()
        response = self.client.delete(reverse('artwork_api:artist_groups'), {"id": artist_group.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(artwork_models.ArtistGroup.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': artist_group.pk})


    def test_delete_nonexisting_artist_group(self):
        response = self.client.delete(reverse('artwork_api:artist_groups'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_noexisting_artist_group(self):
        response = self.client.put(reverse('artwork_api:artist_groups'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_with_errors_for_privileged_user(self):
        artist_group = ArtistGroupFactory()
        response = self.client.put(reverse('artwork_api:artist_groups'), {"id": artist_group.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"details":{"name":["This field is required."]}})


    def test_update_without_errors_for_privileged_user(self):
        artist_group = ArtistGroupFactory()
        response = self.client.put(reverse('artwork_api:artist_groups'), {"id": artist_group.pk, "name": "Group1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = json.loads(response.content)
        self.assertEqual(response["name"], "Group1")


class ArtistGroupUnpriviligedEndpointTestCase(APITestCase):


    def setUp(self):
        nonadmin_login(self)


    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:artist_groups'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:artist_groups'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_get_collection_of_artist_groups(self):
        response = self.client.get(reverse('artwork_api:artist_groups'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_artist_group(self):
        artist_group = ArtistGroupFactory()
        response = self.client.delete(reverse('artwork_api:artist_groups'), {"id": artist_group.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_nonexisting_artist_group(self):
        response = self.client.delete(reverse('artwork_api:artist_groups'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_noexisting_artist_group(self):
        response = self.client.put(reverse('artwork_api:artist_groups'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_with_errors_for_unprivileged_user(self):
        artist_group = ArtistGroupFactory()
        response = self.client.put(reverse('artwork_api:artist_groups'), {"id": artist_group.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_without_errors_for_unprivileged_user(self):
        artist_group = ArtistGroupFactory()
        response = self.client.put(reverse('artwork_api:artist_groups'), {"id": artist_group.pk, "name": "Group1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


class EquipmentTypePriviligedEndpointTestCase(APITestCase):


    def setUp(self):
        admin_login(self)


    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('artwork_api:equipment_types'))
        self.assertEqual(response.status_code, 200)


    def test_get_collection_of_equipment_type(self):
        EquipmentTypeFactory()
        EquipmentTypeFactory()
        response = self.client.get(reverse('artwork_api:equipment_types'))
        response_content = json.loads(response.content)

        self.assertEqual(response_content['count'], 2)
        self.assertEqual(len(response_content['results']), 2)
        self.assertEqual(response.status_code, 200)

        all_keys = ["count", "next", "previous", "results"]
        object_keys = ["id", "name", "provider", "url", "notes", "created"]
        response_all_keys = response_content.keys()
        response_object_keys = response_content['results'][0].keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
        self.assertEqual(sorted(object_keys), sorted(response_object_keys))


    def test_delete_equipment_type(self):
        equipment_type = EquipmentTypeFactory()
        count = artwork_models.EquipmentType.objects.count()
        response = self.client.delete(reverse('artwork_api:equipment_types'), {"id": equipment_type.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(artwork_models.EquipmentType.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': equipment_type.pk})


    def test_delete_nonexisting_equipment_type(self):
        response = self.client.delete(reverse('artwork_api:equipment_types'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_noexisting_equipment_type(self):
        response = self.client.put(reverse('artwork_api:equipment_types'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_with_errors_for_privileged_user(self):
        equipment_type = EquipmentTypeFactory()
        response = self.client.put(reverse('artwork_api:equipment_types'), {"id": equipment_type.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"details":{"name":["This field is required."]}})


    def test_update_without_errors_for_privileged_user(self):
        equipment_type = EquipmentTypeFactory()
        response = self.client.put(reverse('artwork_api:equipment_types'),
            {"id": equipment_type.pk, "name": "Type1", "provider": "Provider1", "notes": "Notes1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = json.loads(response.content)
        self.assertEqual(response["name"], "Type1")
        self.assertEqual(response["provider"], "Provider1")
        self.assertEqual(response["notes"], "Notes1")


class EquipmentTypeUnpriviligedEndpointTestCase(APITestCase):


    def setUp(self):
        nonadmin_login(self)


    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:equipment_types'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:equipment_types'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_get_collection_of_equipment_type(self):
        response = self.client.get(reverse('artwork_api:equipment_types'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_equipment_type(self):
        equipment_type = EquipmentTypeFactory()
        response = self.client.delete(reverse('artwork_api:equipment_types'), {"id": equipment_type.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_delete_nonexisting_equipment_type(self):
        response = self.client.delete(reverse('artwork_api:equipment_types'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_noexisting_equipment_type(self):
        response = self.client.put(reverse('artwork_api:equipment_types'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_with_errors_for_unprivileged_user(self):
        equipment_type = EquipmentTypeFactory()
        response = self.client.put(reverse('artwork_api:equipment_types'), {"id": equipment_type.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


    def test_update_without_errors_for_unprivileged_user(self):
        equipment_type = EquipmentTypeFactory()
        response = self.client.put(reverse('artwork_api:equipment_types'),
            {"id": equipment_type.pk, "name": "Type1", "provider": "Provider1", "notes": "Notes1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})