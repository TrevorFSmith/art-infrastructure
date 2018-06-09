from django.contrib.auth.models import User
import factory
from lighting import models as lighting_models
from iboot import models as iboot_models
from artwork import models as artwork_models


# For lighting

class ProjectorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = lighting_models.Projector

    name = factory.Sequence(lambda n: 'Projector {}'.format(n))
    pjlink_host = factory.Sequence(lambda n: '10.0.{}.{}'.format(n, n))
    pjlink_port = factory.Sequence(lambda n: '{}'.format(n))
    pjlink_password = "mooo"


class BACNetLightFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = lighting_models.BACNetLight

    name = factory.Sequence(lambda n: 'BACNetLight {}'.format(n))
    device_id = factory.Sequence(lambda n: '{}'.format(n))
    property_id = factory.Sequence(lambda n: '{}'.format(n))


class CrestonFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = lighting_models.Creston

    name = factory.Sequence(lambda n: 'Creston {}'.format(n))
    host = factory.Sequence(lambda n: '10.0.{}.{}'.format(n, n))
    port = factory.Sequence(lambda n: '{}'.format(n))


# For iboot

class IBootFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = iboot_models.IBootDevice

    name = factory.Sequence(lambda n: 'iBoot {}'.format(n))
    mac_address = factory.Sequence(lambda n: '00-0D-AD-01-94-6{}'.format(n))
    host = '127.0.0.1'
    port = 8008


# For artwork

class ArtistFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = artwork_models.Artist

    name = factory.Sequence(lambda n: 'Artist {}'.format(n))
    email = factory.Sequence(lambda n: 'artist{}.example.com'.format(n))
    phone = '111-111-111'
    notes = factory.Sequence(lambda n: 'Notes {}'.format(n))

    @factory.post_generation
    def artist_groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.artistgroup_set.add(group)


class ArtistGroupFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = artwork_models.ArtistGroup

    name = factory.Sequence(lambda n: 'Artist Group {}'.format(n))

    @factory.post_generation
    def artists(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for artist in extracted:
                self.artists.add(artist)


class EquipmentTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = artwork_models.EquipmentType

    name = factory.Sequence(lambda n: 'Equipment Type {}'.format(n))
    provider = factory.Sequence(lambda n: 'Provider {}'.format(n))
    notes = factory.Sequence(lambda n: 'Notes {}'.format(n))


class EquipmentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = artwork_models.Equipment

    name = factory.Sequence(lambda n: 'Equipment {}'.format(n))
    notes = factory.Sequence(lambda n: 'Notes {}'.format(n))
    equipment_type = factory.SubFactory(EquipmentTypeFactory)


class PhotoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = artwork_models.Photo

    image = factory.django.ImageField()
    title = factory.Sequence(lambda n: 'Title {}'.format(n))
    caption = factory.Sequence(lambda n: 'Caption {}'.format(n))
    description = factory.Sequence(lambda n: 'Description {}'.format(n))


class DocumentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = artwork_models.Document

    title = factory.Sequence(lambda n: 'Title {}'.format(n))
    doc = factory.django.FileField()


class InstallationSiteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = artwork_models.InstallationSite

    name = factory.Sequence(lambda n: 'Installation Site {}'.format(n))
    location = factory.Sequence(lambda n: 'Location {}'.format(n))
    notes = factory.Sequence(lambda n: 'Notes {}'.format(n))

    @factory.post_generation
    def photos(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for photo in extracted:
                self.photos.add(photo)

    @factory.post_generation
    def equipment(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for equipment in extracted:
                self.equipment.add(equipment)


class InstallationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = artwork_models.Installation

    name = factory.Sequence(lambda n: 'Installation {}'.format(n))
    notes = factory.Sequence(lambda n: 'Notes {}'.format(n))
    site = factory.SubFactory(InstallationSiteFactory)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)

    @factory.post_generation
    def artists(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for artist in extracted:
                self.artists.add(artist)

    @factory.post_generation
    def user(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.user.add(user)

    @factory.post_generation
    def photos(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for photo in extracted:
                self.photos.add(photo)

    @factory.post_generation
    def documents(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for document in extracted:
                self.documents.add(document)


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'Username {}'.format(n))
    password = "12345678"
