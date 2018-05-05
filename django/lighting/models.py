import datetime
import traceback

from django.db import models

from front.models import EventModel
from pjlink import PJLinkController


class BACNetLight(models.Model):

    """A lighting fixture which is controlled using the BACNet protocols.
    In BACNet speak: we're reading and writing Present-Value on Analog Outputs which range in value from 0 to 100."""
    name = models.CharField(max_length=1024, null=False, blank=False)
    device_id = models.PositiveIntegerField(null=False, blank=False, default=0)
    property_id = models.PositiveIntegerField(null=False, blank=False, default=0)

    @models.permalink
    def get_absolute_url(self):
        return ('lighting.views.bacnet_light', (), { 'id':self.id })

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        ordering = ['name']
        verbose_name = "BACNet Light"
        verbose_name_plural = "BACNet Lights"


class Projector(models.Model):

    """A light projection system which is controlled via the net."""
    name = models.CharField(max_length=1024, null=False, blank=False)
    pjlink_host = models.CharField(max_length=1024, null=False, blank=False)
    pjlink_port = models.IntegerField(null=False, blank=False, default=4352)
    pjlink_password = models.CharField(max_length=512, blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        ordering = ['name']


class ProjectorEvent(EventModel):

    COMMAND_CHOICES = (('on', 'Turn On'), ('off', 'Turn Off'))
    command = models.CharField(max_length=12, blank=False, null=False, choices=COMMAND_CHOICES, default='off')
    device = models.ForeignKey(Projector, blank=False, null=False)

    def execute(self):
        print 'running ', self
        try:
            controller = PJLinkController(host=self.device.pjlink_host, port=self.device.pjlink_port, password=self.device.pjlink_password)
            if self.command == 'on':
                controller.power_on()
            elif self.command == 'off':
                controller.power_off()
            else:
                self.tries = self.tries + 1
                self.save()
                return False
            print 'ran command', self.command
        except:
            traceback.print_exc()
            self.tries = self.tries + 1
            self.save()
            return False

        self.last_run = datetime.datetime.now()
        self.tries = 1
        self.save()
        return True

    def __unicode__(self):
        return 'Projector Event: [%s],[%s],[%s]' % (self.days, self.hours, self.minutes)
