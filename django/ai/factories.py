from django.contrib.auth.models import User
import factory
from lighting import models as lighting_models


class ProjectorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = lighting_models.Projector

    name = factory.Sequence(lambda n: 'Projector {}'.format(n))
    pjlink_host = factory.Sequence(lambda n: '10.0.{}.{}'.format(n, n))
    pjlink_port = factory.Sequence(lambda n: '{}'.format(n))
    pjlink_password = "mooo"
