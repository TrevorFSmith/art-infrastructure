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


class ArtistGroupFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = artwork_models.ArtistGroup

    name = factory.Sequence(lambda n: 'Artist Group {}'.format(n))


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