import datetime
import traceback

from django.db import models
from django.utils import timezone

from front.models import EventModel
from pjlink import PJLinkController
from creston import CrestonControl


class BACNetLight(models.Model):

    """A lighting fixture which is controlled using the BACNet protocols.
    In BACNet speak: we're reading and writing Present-Value on Analog Outputs which range in value from 0 to 100."""
    name = models.CharField(max_length=1024, null=False, blank=False)
    device_id = models.PositiveIntegerField(null=False, blank=False, default=0)
    property_id = models.PositiveIntegerField(null=False, blank=False, default=0)
    status = models.BooleanField(default=False)

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
    status = models.BooleanField(default=False)

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

        self.last_run = datetime.datetime.now(timezone.utc)
        self.tries = 1
        self.save()
        return True

    def __unicode__(self):
        return 'Projector Event: [%s],[%s],[%s]' % (self.days, self.hours, self.minutes)


class Creston(models.Model):

    name = models.CharField(max_length=1024, null=False, blank=False)
    host = models.CharField(max_length=1024, null=False, blank=False)
    port = models.IntegerField(null=False, blank=False, default=1313)
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        ordering = ['name']


class CrestonEvent(EventModel):

    COMMAND_CHOICES = (
        ('Ping', 'Ping'),
        ('Update', 'Query system'),
        #('Help', 'For help with list of Commands'),
        ('EnableDim', 'Dim On/Off Toggle'),
        ('DimLvlUp', 'To adjust the Dim sensitivity up'),
        ('DimLvlDown', 'To adjust the Dim sensitivity down'),
        ('EnableHigh', 'High On/Off Toggle'),
        ('HighLvlUp', 'To adjust the high sensitivity brightness up'),
        ('HighLvlDown', 'To adjust the high sensitivity brightness down'),
        ('MemoryStore', 'To store a Dim and High memory preset level'),
        ('MemoryRecall', 'To recall a Dim and High memory preset level'),
        ('Display1On', 'To turn on the left projector'),
        ('Display1Off', 'To turn off the left projector'),
        ('Display1DVI', 'To view DVI Input on left projector'),
        ('Display1HighBright', 'To adjust the image brightness of the left projector to its highest level'),
        ('Display1LowBright', 'To adjust the image brightness of the left projector to its lowest level'),
        ('Display2On', 'To turn on the right projector'),
        ('Display2Off', 'To turn off the right projector'),
        ('Display2DVI', 'To view DVI input on right projector'),
        ('Display2HighBright', 'To adjust the image brightness of the right projector to its highest level'),
        ('Display2LowBright', 'To adjust the image brightness of the right projector to its lowest level'),
        ('WakeEnable', 'This is to set a specified time for projectors to power On/Off Toggle'),
        ('WakeHrUp', 'To adjust the hour parameter up for turning on the system'),
        ('WakeHrDown', 'To adjust the hour parameter down for turning on the system'),
        ('WakeMinUp', 'To adjust the minute parameter up for turning on the system'),
        ('WakeMinDown', 'To adjust the minute parameter down for turning on the system'),
        ('SleepEnable', 'Projector power timer to set powering down of both projectors after a specified amount of time'),
        ('SleepHrUp', 'To adjust the hour parameter up for the projector sleep function'),
        ('SleepHrDown', 'To adjust the hour parameter down for the projector sleep function'),
        ('SleepMinUp', 'To adjust the minute parameter up for the projector sleep function'),
        ('SleepMinDown', 'To adjust the minute parameter down for the projector sleep function'),
    )
    commands = [cmd[0] for cmd in COMMAND_CHOICES]
    command = models.CharField(max_length=20, blank=False, null=False, choices=COMMAND_CHOICES, default='off')
    device = models.ForeignKey(Creston, blank=False, null=False)

    def execute(self):
        print 'running ', self
        try:
            lines = 1
            control = CrestonControl(self.device.host, self.device.port)
            if self.command not in self.commands:
                self.tries = self.tries + 1
                self.save()
                return False
            if self.command == 'Update':
                lines = 9
            control.send_command(self.command, lines)
            print 'ran command', self.command
        except:
            traceback.print_exc()
            self.tries = self.tries + 1
            self.save()
            return False

        self.last_run = datetime.datetime.now(timezone.utc)
        self.tries = 1
        self.save()
        return True

    def __unicode__(self):
        return 'Creston Event: [%s],[%s],[%s]' % (self.days, self.hours, self.minutes)