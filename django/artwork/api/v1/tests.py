from django.test import TestCase, LiveServerTestCase
from django.core.urlresolvers import reverse
#from django.core.files.uploadedfile import SimpleUploadedFile
from ai.factories import *
from ai.test_helpers import *
from django.db import IntegrityError
from selenium.common.exceptions import NoSuchElementException

from rest_framework import status
from rest_framework.test import APITestCase
import json

from artwork import models as artwork_models


# ------------------------------ For Artist ------------------------------

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
        group1 = ArtistGroupFactory()
        group2 = ArtistGroupFactory()
        artist = ArtistFactory()
        response = self.client.put(reverse('artwork_api:artists'),
            {"id": artist.pk, "name": "Artist1", "email": "artist1.example.com", 
            "phone": "111-111-111", "notes": "Notes1", "artistgroup_set": (group1.id, group2.id)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = json.loads(response.content)
        self.assertEqual(response["name"], "Artist1")
        self.assertEqual(response["email"], "artist1.example.com")
        self.assertEqual(response["phone"], "111-111-111")
        self.assertEqual(response["notes"], "Notes1")
        self.assertEqual(response["artistgroup_set"], [group1.id, group2.id])
        response_groups = response["groups_info"]
        self.assertEqual(len(response_groups), 2)
        self.assertEqual(response_groups[0], {"id": group1.id, "name": group1.name})
        self.assertEqual(response_groups[1], {"id": group2.id, "name": group2.name})


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


# ------------------------------ For ArtistGroup ------------------------------

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
        artist1 = ArtistFactory()
        artist2 = ArtistFactory()
        artist_group = ArtistGroupFactory()
        response = self.client.put(reverse('artwork_api:artist_groups'), 
                                   {"id": artist_group.pk, "name": "Group1", "artists": [artist1.id, artist2.id]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = json.loads(response.content)
        self.assertEqual(response["name"], "Group1")
        self.assertEqual(response["artists"], [artist1.id, artist2.id])
        response_artists = response["artists_info"]
        self.assertEqual(len(response_artists), 2)
        self.assertEqual(response_artists[0], {"id": artist1.id, "name": artist1.name})
        self.assertEqual(response_artists[1], {"id": artist2.id, "name": artist2.name})



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


# ------------------------------ For EquipmentType ------------------------------

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


# ------------------------------ For Equipment ------------------------------

class EquipmentPriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        admin_login(self)

    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('artwork_api:equipments'))
        self.assertEqual(response.status_code, 200)

    def test_get_collection_of_equipments(self):
        EquipmentFactory()
        EquipmentFactory()
        response = self.client.get(reverse('artwork_api:equipments'))
        response_content = json.loads(response.content)

        self.assertEqual(response_content['count'], 2)
        self.assertEqual(len(response_content['results']), 2)
        self.assertEqual(response.status_code, 200)

        all_keys = ["count", "next", "previous", "results"]
        object_keys = ["id", "name", "equipment_type", "equipment_type_name", "photos", "photos_info", "notes", "created"]
        response_all_keys = response_content.keys()
        response_object_keys = response_content['results'][0].keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
        self.assertEqual(sorted(object_keys), sorted(response_object_keys))

    def test_delete_equipment(self):
        equipment = EquipmentFactory()
        count = artwork_models.Equipment.objects.count()
        response = self.client.delete(reverse('artwork_api:equipments'), {"id": equipment.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(artwork_models.Equipment.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': equipment.pk})

    def test_delete_nonexisting_equipment(self):
        response = self.client.delete(reverse('artwork_api:equipments'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_noexisting_equipment(self):
        response = self.client.put(reverse('artwork_api:equipments'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_errors_for_privileged_user(self):
        equipment = EquipmentFactory()
        response = self.client.put(reverse('artwork_api:equipments'), {"id": equipment.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),
                         {"details":{"name":["This field is required."],
                                     "equipment_type":["This field is required."]}})

    def test_update_without_errors_for_privileged_user(self):
        equipment_type = EquipmentTypeFactory()
        photo1 = PhotoFactory()
        photo2 = PhotoFactory()
        equipment = EquipmentFactory()
        response = self.client.put(reverse('artwork_api:equipments'),
            {"id": equipment.pk, "name": "New Equipment", 
             "equipment_type": equipment_type.id, "photos": (photo1.id, photo2.id), "notes": "Note1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = json.loads(response.content)
        self.assertEqual(response["name"], "New Equipment")
        self.assertEqual(response["equipment_type"], equipment_type.id)
        self.assertEqual(response["photos"], [photo2.id, photo1.id])
        self.assertEqual(response["notes"], "Note1")
        self.assertEqual(response["equipment_type_name"], equipment_type.name)
        response_photos = response["photos_info"]
        self.assertEqual(len(response_photos), 2)
        self.assertEqual(response_photos[0], {"id": photo2.id, "image": photo2.image.name, "title": photo2.title})
        self.assertEqual(response_photos[1], {"id": photo1.id, "image": photo1.image.name, "title": photo1.title})


class EquipmentUnpriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        nonadmin_login(self)

    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:equipments'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:equipments'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_collection_of_equipments(self):
        response = self.client.get(reverse('artwork_api:equipments'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_equipment(self):
        equipment = EquipmentFactory()
        response = self.client.delete(reverse('artwork_api:equipments'), {"id": equipment.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_nonexisting_equipment(self):
        response = self.client.delete(reverse('artwork_api:equipments'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_noexisting_equipment(self):
        response = self.client.put(reverse('artwork_api:equipments'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_with_errors_for_unprivileged_user(self):
        equipment = EquipmentFactory()
        response = self.client.put(reverse('artwork_api:equipments'), {"id": equipment.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_without_errors_for_unprivileged_user(self):
        equipment_type = EquipmentTypeFactory()
        equipment = EquipmentFactory()
        response = self.client.put(reverse('artwork_api:equipments'),
            {"id": equipment.pk, "name": "New Equipment", "equipment_type": equipment_type.id, "photos": [], "notes": "Note1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


# ------------------------------ For Photo ------------------------------

from django.core.files.storage import FileSystemStorage

class PhotoPriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        admin_login(self)

    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('artwork_api:photos'))
        self.assertEqual(response.status_code, 200)

    def test_get_collection_of_photos(self):
        PhotoFactory()
        PhotoFactory()
        response = self.client.get(reverse('artwork_api:photos'))
        response_content = json.loads(response.content)

        self.assertEqual(response_content['count'], 2)
        self.assertEqual(len(response_content['results']), 2)
        self.assertEqual(response.status_code, 200)

        all_keys = ["count", "next", "previous", "results"]
        object_keys = ["id", "image", "title", "caption", "description", "created"]

        response_all_keys = response_content.keys()
        response_object_keys = response_content['results'][0].keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
        self.assertEqual(sorted(object_keys), sorted(response_object_keys))

    def test_delete_photo(self):
        photo = PhotoFactory()
        count = artwork_models.Photo.objects.count()
        response = self.client.delete(reverse('artwork_api:photos'), {"id": photo.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(artwork_models.Photo.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': photo.pk})

    def test_delete_nonexisting_photo(self):
        response = self.client.delete(reverse('artwork_api:photos'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_noexisting_photo(self):
        response = self.client.put(reverse('artwork_api:photos'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_errors_for_privileged_user(self):
        photo = PhotoFactory()
        response = self.client.put(reverse('artwork_api:photos'), {"id": photo.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"details":{"image":["No file was submitted."]}})

    # def test_update_without_errors_for_privileged_user(self):
    #     photo = PhotoFactory()
    #     image = SimpleUploadedFile(name=photo.image.name, content=photo.image.read(), content_type='image/jpeg')
    #     response = self.client.put(reverse('artwork_api:photos'),
    #         {"id": photo.pk, "image": image, "title": "Title1", "caption": "Caption1", "description": "Desc1"})

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     response = json.loads(response.content)
    #     self.assertEqual(response["title"], "Title1")
    #     self.assertEqual(response["caption"], "Caption1")
    #     self.assertEqual(response["description"], "Desc1")


class PhotoUnpriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        nonadmin_login(self)

    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:photos'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:photos'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_collection_of_photos(self):
        response = self.client.get(reverse('artwork_api:photos'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_photo(self):
        photo = PhotoFactory()
        response = self.client.delete(reverse('artwork_api:photos'), {"id": photo.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_nonexisting_photo(self):
        response = self.client.delete(reverse('artwork_api:photos'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_noexisting_photo(self):
        response = self.client.put(reverse('artwork_api:photos'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_with_errors_for_unprivileged_user(self):
        photo = PhotoFactory()
        response = self.client.put(reverse('artwork_api:photos'), {"id": photo.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_without_errors_for_unprivileged_user(self):
        photo = PhotoFactory()
        response = self.client.put(reverse('artwork_api:photos'),
            {"id": photo.pk, "image": photo.image, "title": "Title1", "caption": "Caption1", "description": "Desc1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


# ------------------------------ For Document ------------------------------

class DocumentPriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        admin_login(self)

    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('artwork_api:documents'))
        self.assertEqual(response.status_code, 200)

    def test_get_collection_of_documents(self):
        DocumentFactory()
        DocumentFactory()
        response = self.client.get(reverse('artwork_api:documents'))
        response_content = json.loads(response.content)

        self.assertEqual(response_content['count'], 2)
        self.assertEqual(len(response_content['results']), 2)
        self.assertEqual(response.status_code, 200)

        all_keys = ["count", "next", "previous", "results"]
        object_keys = ["id", "title", "doc", "created"]
        response_all_keys = response_content.keys()
        response_object_keys = response_content['results'][0].keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
        self.assertEqual(sorted(object_keys), sorted(response_object_keys))

    def test_delete_document(self):
        document = DocumentFactory()
        count = artwork_models.Document.objects.count()
        response = self.client.delete(reverse('artwork_api:documents'), {"id": document.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(artwork_models.Document.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': document.pk})

    def test_delete_nonexisting_document(self):
        response = self.client.delete(reverse('artwork_api:documents'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_noexisting_document(self):
        response = self.client.put(reverse('artwork_api:documents'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_errors_for_privileged_user(self):
        document = DocumentFactory()
        response = self.client.put(reverse('artwork_api:documents'), {"id": document.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"details":{"doc":["No file was submitted."]}})

    # def test_update_without_errors_for_privileged_user(self):
    #     document = DocumentFactory()
    #     response = self.client.put(reverse('artwork_api:documents'),
    #         {"id": document.pk, "title": "Document1", "doc": document.doc})

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     response = json.loads(response.content)
    #     self.assertEqual(response["title"], "Document1")


class DocumentUnpriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        nonadmin_login(self)

    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:documents'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:documents'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_collection_of_documents(self):
        response = self.client.get(reverse('artwork_api:documents'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_document(self):
        document = DocumentFactory()
        response = self.client.delete(reverse('artwork_api:documents'), {"id": document.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_nonexisting_document(self):
        response = self.client.delete(reverse('artwork_api:documents'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_noexisting_document(self):
        response = self.client.put(reverse('artwork_api:documents'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_with_errors_for_unprivileged_user(self):
        document = DocumentFactory()
        response = self.client.put(reverse('artwork_api:documents'), {"id": document.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_without_errors_for_unprivileged_user(self):
        document = DocumentFactory()
        response = self.client.put(reverse('artwork_api:documents'),
            {"id": document.pk, "title": "Document1", "doc": document.doc})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


# ------------------------------ For InstallationSite ------------------------------

class InstallationSitePriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        admin_login(self)

    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('artwork_api:installation_sites'))
        self.assertEqual(response.status_code, 200)

    def test_get_collection_of_installation_sites(self):
        InstallationSiteFactory()
        InstallationSiteFactory()
        response = self.client.get(reverse('artwork_api:installation_sites'))
        response_content = json.loads(response.content)

        self.assertEqual(response_content['count'], 2)
        self.assertEqual(len(response_content['results']), 2)
        self.assertEqual(response.status_code, 200)

        all_keys = ["count", "next", "previous", "results"]
        object_keys = ["id", "name", "location", "notes", "photos", "photos_info", "equipment", "equipment_info", "created"]
        response_all_keys = response_content.keys()
        response_object_keys = response_content['results'][0].keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
        self.assertEqual(sorted(object_keys), sorted(response_object_keys))

    def test_delete_installation_site(self):
        installation_site = InstallationSiteFactory()
        count = artwork_models.InstallationSite.objects.count()
        response = self.client.delete(reverse('artwork_api:installation_sites'), {"id": installation_site.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(artwork_models.InstallationSite.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': installation_site.pk})

    def test_delete_nonexisting_installation_site(self):
        response = self.client.delete(reverse('artwork_api:installation_sites'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_noexisting_installation_site(self):
        response = self.client.put(reverse('artwork_api:installation_sites'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_errors_for_privileged_user(self):
        installation_site = InstallationSiteFactory()
        response = self.client.put(reverse('artwork_api:installation_sites'), {"id": installation_site.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"details":{"name":["This field is required."]}})

    def test_update_without_errors_for_privileged_user(self):
        photo1 = PhotoFactory()
        photo2 = PhotoFactory()
        equipment1 = EquipmentFactory()
        equipment2 = EquipmentFactory()
        installation_site = InstallationSiteFactory()
        response = self.client.put(reverse('artwork_api:installation_sites'),
            {"id": installation_site.pk, "name": "InstallationSite1", "location": "location1", "notes": "notes1", 
            "photos": (photo1.id, photo2.id), "equipment": (equipment1.id, equipment2.id)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = json.loads(response.content)
        self.assertEqual(response["name"], "InstallationSite1")
        self.assertEqual(response["location"], "location1")
        self.assertEqual(response["notes"], "notes1")
        self.assertEqual(response["photos"], [photo2.id, photo1.id])
        self.assertEqual(response["equipment"], [equipment1.id, equipment2.id])
        response_photos = response["photos_info"]
        self.assertEqual(len(response_photos), 2)
        self.assertEqual(response_photos[0], {"id": photo2.id, "image": photo2.image.name, "title": photo2.title})
        self.assertEqual(response_photos[1], {"id": photo1.id, "image": photo1.image.name, "title": photo1.title})
        response_equipment = response["equipment_info"]
        self.assertEqual(len(response_equipment), 2)
        self.assertEqual(response_equipment[0], {"id": equipment1.id, "name": equipment1.name})
        self.assertEqual(response_equipment[1], {"id": equipment2.id, "name": equipment2.name})


class InstallationSiteUnpriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        nonadmin_login(self)

    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:installation_sites'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:installation_sites'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_collection_of_installation_sites(self):
        response = self.client.get(reverse('artwork_api:installation_sites'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_installation_site(self):
        installation_site = InstallationSiteFactory()
        response = self.client.delete(reverse('artwork_api:installation_sites'), {"id": installation_site.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_nonexisting_installation_site(self):
        response = self.client.delete(reverse('artwork_api:installation_sites'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_noexisting_installation_site(self):
        response = self.client.put(reverse('artwork_api:installation_sites'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_with_errors_for_unprivileged_user(self):
        installation_site = InstallationSiteFactory()
        response = self.client.put(reverse('artwork_api:installation_sites'), {"id": installation_site.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_without_errors_for_unprivileged_user(self):
        installation_site = InstallationSiteFactory()
        response = self.client.put(reverse('artwork_api:installation_sites'),
            {"id": installation_site.pk, "name": "InstallationSite1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})


# ------------------------------ For Installation ------------------------------

class InstallationPriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        admin_login(self)

    def test_get_200_for_privileged_user(self):
        response = self.client.get(reverse('artwork_api:installations'))
        self.assertEqual(response.status_code, 200)

    def test_get_collection_of_installations(self):
        InstallationFactory()
        InstallationFactory()
        response = self.client.get(reverse('artwork_api:installations'))
        response_content = json.loads(response.content)

        self.assertEqual(response_content['count'], 2)
        self.assertEqual(len(response_content['results']), 2)
        self.assertEqual(response.status_code, 200)

        all_keys = ["count", "next", "previous", "results"]
        object_keys = ["id", "name", "groups", "artists", "user", "site", "opened", "closed", "notes", "photos", 
            "documents", "created", "site_name", "groups_info", "artists_info", "users_info", "photos_info", "documents_info"]
        response_all_keys = response_content.keys()
        response_object_keys = response_content['results'][0].keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
        self.assertEqual(sorted(object_keys), sorted(response_object_keys))

    def test_delete_installation(self):
        installation = InstallationFactory()
        count = artwork_models.Installation.objects.count()
        response = self.client.delete(reverse('artwork_api:installations'), {"id": installation.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(artwork_models.Installation.objects.count(), count-1)
        self.assertEqual(json.loads(response.content), {u'id': installation.pk})

    def test_delete_nonexisting_installation(self):
        response = self.client.delete(reverse('artwork_api:installations'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_noexisting_installation(self):
        response = self.client.put(reverse('artwork_api:installations'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_errors_for_privileged_user(self):
        installation = InstallationFactory()
        response = self.client.put(reverse('artwork_api:installations'), {"id": installation.pk})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"details":{"name":["This field is required."]}})

    def test_update_without_errors_for_privileged_user(self):
        site = InstallationSiteFactory()
        group1 = ArtistGroupFactory()
        group2 = ArtistGroupFactory()
        artist1 = ArtistFactory()
        artist2 = ArtistFactory()
        user1 = UserFactory()
        user2 = UserFactory()
        photo1 = PhotoFactory()
        photo2 = PhotoFactory()
        document1 = DocumentFactory()
        document2 = DocumentFactory()
        installation = InstallationFactory()
        response = self.client.put(reverse('artwork_api:installations'),
            {"id": installation.pk, "name": "Installation1", "notes": "Note1", "site": site.id,
             "groups": (group1.id, group2.id), "artists": (artist1.id, artist2.id), "user": (user1.id, user2.id),
             "photos": (photo1.id, photo2.id), "documents": (document1.id, document2.id)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = json.loads(response.content)
        self.assertEqual(response["name"], "Installation1")
        self.assertEqual(response["notes"], "Note1")
        self.assertEqual(response["site"], site.id)
        self.assertEqual(response["site_name"], site.name)
        self.assertEqual(response["groups"], [group1.id, group2.id])
        self.assertEqual(response["artists"], [artist1.id, artist2.id])
        self.assertEqual(response["user"], [user1.id, user2.id])
        self.assertEqual(response["photos"], [photo2.id, photo1.id])
        self.assertEqual(response["documents"], [document2.id, document1.id])
        response_groups = response["groups_info"]
        self.assertEqual(len(response_groups), 2)
        self.assertEqual(response_groups[0], {"id": group1.id, "name": group1.name})
        self.assertEqual(response_groups[1], {"id": group2.id, "name": group2.name})
        response_artists = response["artists_info"]
        self.assertEqual(len(response_artists), 2)
        self.assertEqual(response_artists[0], {"id": artist1.id, "name": artist1.name})
        self.assertEqual(response_artists[1], {"id": artist2.id, "name": artist2.name})
        response_users = response["users_info"]
        self.assertEqual(len(response_users), 2)
        self.assertEqual(response_users[0], {"id": user1.id, "username": user1.username})
        self.assertEqual(response_users[1], {"id": user2.id, "username": user2.username})
        response_photos = response["photos_info"]
        self.assertEqual(len(response_photos), 2)
        self.assertEqual(response_photos[0], {"id": photo2.id, "image": photo2.image.name, "title": photo2.title})
        self.assertEqual(response_photos[1], {"id": photo1.id, "image": photo1.image.name, "title": photo1.title})
        response_documents = response["documents_info"]
        self.assertEqual(len(response_documents), 2)
        self.assertEqual(response_documents[0], {"id": document2.id, "title": document2.title, "doc": document2.doc.name})
        self.assertEqual(response_documents[1], {"id": document1.id, "title": document1.title, "doc": document1.doc.name})


class InstallationUnpriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        nonadmin_login(self)

    def test_get_403_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:installations'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_200_for_unprivileged_user(self):
        response = self.client.get(reverse('artwork_api:installations'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_collection_of_installations(self):
        response = self.client.get(reverse('artwork_api:installations'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_installation(self):
        installation = InstallationFactory()
        response = self.client.delete(reverse('artwork_api:installations'), {"id": installation.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_delete_nonexisting_installation(self):
        response = self.client.delete(reverse('artwork_api:installations'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_noexisting_installation(self):
        response = self.client.put(reverse('artwork_api:installations'), {"id": 555})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_with_errors_for_unprivileged_user(self):
        installation = InstallationFactory()
        response = self.client.put(reverse('artwork_api:installations'), {"id": installation.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_update_without_errors_for_unprivileged_user(self):
        installation = InstallationFactory()
        response = self.client.put(reverse('artwork_api:installations'), {"id": installation.pk, "name": "Installation1"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})