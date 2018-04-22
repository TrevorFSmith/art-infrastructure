from __future__ import unicode_literals
from datetime import timedelta

from django.db import models
from django.utils import timezone

from artwork.models import Installation


class HeartbeatManager(models.Manager):

    def delete_old_heartbeats(self):
        deadline = timezone.now() - timedelta(days=2)
        for heartbeat in self.filter(created__lt=deadline):
            heartbeat.delete()


class Heartbeat(models.Model):

    """A periodic message sent by an installation which is used to monitor their status."""
    installation = models.ForeignKey(Installation, null=False, blank=False)
    info = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = HeartbeatManager()

    def trimmed_info(self):
        if self.info:
            if len(self.info) > 60:
                return self.info[:60] + '...'
            return self.info
        return None

    def timed_out(self):
        return self.created + timedelta(seconds=settings.HEARTBEAT_TIMEOUT) < timezone.now()

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return "%s: %s" % (self.installation, self.created)
