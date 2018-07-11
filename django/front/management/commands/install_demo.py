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
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from rest_framework.authtoken.models import Token

from weather.models import WeatherInfo
from lighting.models import BACNetLight, Creston, Projector
from iboot.models import IBootDevice
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



class Command(BaseCommand):

    help = "Installs the demo data."

    def handle(self, *labels, **options):

        if settings.PRODUCTION:
            print 'I will not install the demo on a PRODUCTION machine.  Sorry.'
            return

        call_command('migrate', interactive=False)

        WeatherInfo.objects.all().delete()
        Token.objects.all().delete()

        site = Site.objects.get_current()
        site.domain = '127.0.0.1:8000'
        site.name = 'Art Infrastructure'
        site.save()

        users=[]
        User.objects.all().delete()
        users.append(self.create_user('trevor', '1234', 'trevor@example.com', 'Trevor F.', 'Smith', True, True))
        users.append(self.create_user('matt', '1234', 'matt@example.com', 'Matt', 'Gorbet', True, True))

        artist_names = ['Anthony Jones', 'Davone Smith', 'Wendy Doe', 'Jasmin Hense', 'Steph Able', 'Moon Unit Alpha',
                        'Henderson Blake', 'Richardson William', 'Armstrong Joel', 'Goodwin Joshua', 'Spencer Joseph', 'Clark Brett']
        locations    = ['Seattle Tacoma International Airport', 'Kiev Zhuliany International Airport', 
                        'London Airport', 'Paris Municipal Airport', 'Pekin Municipal Airport', 
                        'Berlin Regional Airport', 'Brazil Clay County Airport', 'General La Madrid Airport', 
                        'Milan Airport', 'Sidney Municipal Airport']

        artists            = self.create_artists(artist_names)
        artist_groups      = self.create_groups((artists[0:2], artists[2:5], artists[5:9], artists[9:len(artists)]))
        photos             = self.create_photos()
        documents          = self.create_documents()
        bacnet_lights      = self.create_bacnet_lights()
        projectors         = self.create_projectors()
        crestons           = self.create_crestons()
        iboots             = self.create_iboots()
        equipment_types    = self.create_equipment_types()
        equipments         = self.create_equipments(equipment_types, bacnet_lights, projectors, crestons, iboots, photos)
        installation_sites = self.create_installation_site(locations, photos, equipments)
        installations      = self.create_installations(artist_groups, artists, users, installation_sites, photos, documents)

    def create_user(self, username, password, email, first_name=None, last_name=None, is_staff=False, is_superuser=False):
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name,
                                   email=email, is_staff=is_staff, is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user

    def create_bacnet_lights(self):
        BACNetLight.objects.all().delete()
        bacnet_light_name = "Light"
        bacnet_lights = []
        for i in range(1, 11):
            bacnet_light = BACNetLight.objects.create(name=bacnet_light_name + str(i), device_id=i, property_id=i)
            bacnet_lights.append(bacnet_light)
        return bacnet_lights

    def create_projectors(self):
        Projector.objects.all().delete()
        projector_name = "Projector"
        projectors = []
        for i in range(1, 11):
            projector = Projector.objects.create(name=projector_name + str(i), pjlink_host='127.0.0.1', pjlink_port=4352)
            projectors.append(projector)
        return projectors

    def create_crestons(self):
        Creston.objects.all().delete()
        creston_name = "Creston"
        crestons = []
        for i in range(1, 11):
            creston = Creston.objects.create(name=creston_name + str(i), host='127.0.0.1', port=1313)
            crestons.append(creston)
        return crestons

    def create_iboots(self):
        IBootDevice.objects.all().delete()
        iboot_name = "iBoot"
        iboots = []
        for i in range(1, 11):
            iboot = IBootDevice.objects.create(name=iboot_name + str(i), mac_address='00-0D-AD-01-94-6F',
                                               host='127.0.0.1', port=8008)
            iboots.append(iboot)
        return iboots

    def create_artists(self, artist_names):
        Artist.objects.all().delete()
        artist_emails = self.get_artist_emails(artist_names)
        artists = []
        for i in range(len(artist_names)):
            artists.append(Artist.objects.create(name=artist_names[i], email=artist_emails[i], 
                                                 phone='206-555-1212', url='http://example.com/'))
        return artists

    def create_groups(self, artists_in_groups):
        ArtistGroup.objects.all().delete()
        group_name = "Group"
        count = 1
        artist_groups = []
        for artists in artists_in_groups:
            artist_group = ArtistGroup.objects.create(name=group_name + str(count), url='http://example.com/')
            for artist in artists:
                artist_group.artists.add(artist)
            artist_groups.append(artist_group)
            count += 1
        return artist_groups

    def create_photos(self):
        Photo.objects.all().delete()
        photo_title = "Photo"
        photo_caption = "Caption"
        photo_description = "Description"
        photos = []
        for i in range(1, 11):
            img = open("./front/management/commands/imgs/img{0}.jpg".format(i), "r")
            photo = Photo.objects.create(title=photo_title + str(i), image=File(img), 
                                         caption=photo_caption + str(i), description=photo_description + str(i))
            photos.append(photo)
        return photos

    def create_documents(self):
        Document.objects.all().delete()
        document_title = "Document"
        documents = []
        for i in range(1, 11):
            doc = open("./front/management/commands/documents/document{0}.txt".format(i), "r")
            document = Document.objects.create(title=document_title + str(i), doc=File(doc))
            documents.append(document)
        return documents

    def create_equipment_types(self):
        EquipmentType.objects.all().delete()
        equipment_type_name = "EquipmentType"
        equipment_type_note = "Note"
        equipment_types = []
        for i in range(1, 11):
            equipment_type = EquipmentType.objects.create(name=equipment_type_name + str(i), provider=i,
                                                          url='http://example.com/', notes=equipment_type_note + str(i))
            equipment_types.append(equipment_type)
        return equipment_types

    def get_artist_emails(self, artist_names):
        artist_emails = []
        for artist_name in artist_names:
            values = artist_name.split(" ")
            initials = ""
            for value in values:
                initials += value[0]
            artist_emails.append(initials.lower() + '@example.com')
        return artist_emails

    def create_equipments(self, equipment_types, bacnet_lights, projectors, crestons, iboots, photos):
        Equipment.objects.all().delete()
        equipment_name = "Equipment"
        equipment_note = "Note"
        photo_count = 0
        quant = 2
        equipments = []
        for i in range(0, 10):
            devices = []
            if not i % 2:
                devices = iboots
            elif not i % 3:
                devices = crestons
            elif not i % 5:
                devices = projectors
            else:
                devices = bacnet_lights
            ct = ContentType.objects.get_for_model(devices[0].__class__)
            equipment_type = equipment_types[i] if i < len(equipment_types) else equipment_types[0]
            device = devices[i] if i < len(devices) else devices[0]
            if (photo_count + quant) > len(photos): photo_count = 0
            equipment_photos = photos[photo_count:(photo_count + quant)]
            photo_count += quant
            equipment = Equipment.objects.create(name=equipment_name + str(i + 1), equipment_type=equipment_type,
                                                 device_type=ct, device_id=device.id, notes=equipment_note + str(i + 1))
            for photo in equipment_photos:
                equipment.photos.add(photo)
            equipments.append(equipment)
        return equipments

    def create_installation_site(self, locations, photos, equipments):
        InstallationSite.objects.all().delete()
        installation_site_name = "InstallationSite"
        installation_site_note = "Note"
        photo_count     = 0
        equipment_count = 0
        quant = 2
        installation_sites = []
        for i in range(0, 10):
            installation_site_location = locations[i] if i < len(locations) else locations[0]
            if (photo_count + quant) > len(photos): photo_count = 0
            installation_site_photos = photos[photo_count:(photo_count + quant)]
            photo_count += quant
            if (equipment_count + quant) > len(equipments): equipment_count = 0
            installation_site_equipments = equipments[equipment_count:(equipment_count + quant)]
            equipment_count += quant
            installation_site = InstallationSite.objects.create(name=installation_site_name + str(i + 1),
                                                                location=installation_site_location,
                                                                notes=installation_site_note + str(i + 1))
            for photo in installation_site_photos:
                installation_site.photos.add(photo)
            for equipment in installation_site_equipments:
                installation_site.equipment.add(equipment)
            installation_sites.append(installation_site)
        return installation_sites

    def create_installations(self, artist_groups, artists, users, installation_sites, photos, documents):
        Installation.objects.all().delete()
        installation_name = "Installation"
        installation_note = "Note"
        artist_group_count = 0
        artist_count       = 0
        user_count         = 0
        photo_count        = 0
        document_count     = 0
        quant = 2
        installations = []
        for i in range(0, 10):
            installation_site = installation_sites[i] if i < len(installation_sites) else installation_sites[0]
            if (artist_group_count + quant) > len(artist_groups): artist_group_count = 0
            if (artist_count + quant) > len(artists): artist_count = 0
            if (user_count + quant) > len(users): user_count = 0
            if (photo_count + quant) > len(photos): photo_count = 0
            if (document_count + quant) > len(documents): document_count = 0
            installations_groups    = artist_groups[artist_group_count:(artist_group_count + quant)]
            installations_artists   = artists[artist_count:(artist_count + quant)]
            installations_users     = users[user_count:(user_count + quant)]
            installations_photos    = photos[photo_count:(photo_count + quant)]
            installations_documents = documents[document_count:(document_count + quant)]
            user_count         += quant
            photo_count        += quant
            document_count     += quant
            artist_group_count += quant
            artist_count       += quant
            installation = Installation.objects.create(name=installation_name + str(i + 1), site=installation_site,
                                                       notes=installation_note + str(i + 1))
            for group in installations_groups: installation.groups.add(group)
            for artist in installations_artists: installation.artists.add(artist)
            for user in installations_users: installation.user.add(user)
            for photo in installations_photos: installation.photos.add(photo)
            for document in installations_documents: installation.documents.add(document)
            installations.append(installation)
        return installations