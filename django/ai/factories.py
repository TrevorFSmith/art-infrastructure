from django.contrib.auth.models import User
import factory
from lighting import models as lighting_models
from iboot import models as iboot_models


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


class IBootFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = iboot_models.IBootDevice

    name = factory.Sequence(lambda n: 'iBoot {}'.format(n))
    mac_address = factory.Sequence(lambda n: '00-0D-AD-01-94-6{}'.format(n))
    host = '127.0.0.1'
    port = 8008