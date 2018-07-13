from __future__ import unicode_literals

import re
import os
import time
import urllib
import random
import os.path
import httplib
import datetime
import calendar

import logging
import traceback
import feedparser
import unicodedata
from PIL import Image

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.dispatch import dispatcher
from django.core.mail import send_mail
from django.utils.encoding import force_unicode
from django.db.models import Q


class EventModel(models.Model):
    """
    An abstract base class for models representing recurring scheduled events.

    The days, hours and minutes fields store a comma separated list of 0 based indices into these arrays:
    [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
    [0 to 23]
    [0 to 59]

    So, to schedule an event for Monday and Wednesday at 1:30pm you would set the days, hours, and minutes to [1,3], [13] and [30].
    """

    active = models.BooleanField(blank=False, null=False, default=True)

    days = models.CharField(max_length=120, blank=True, null=True, validators=[validate_comma_separated_integer_list])
    hours = models.CharField(max_length=120, blank=True, null=True, validators=[validate_comma_separated_integer_list])
    minutes = models.CharField(max_length=120, blank=True, null=True, validators=[validate_comma_separated_integer_list])

    last_run = models.DateTimeField(blank=True, null=True, editable=False)
    tries = models.IntegerField(blank=False, null=False, default=0, editable=False)

    def time_description(self):
        if not self.days:
            result = 'Every day'
        else:
            result = 'Every %s' % ', '.join([self.day_number_to_name(i) for i in to_array(self.days)])
        hrs = to_array(self.hours)
        if not hrs:
            result += ' at every hour'
        else:
            if len(hrs) > 1:
                p = 's'
            else:
                p = ''
            result += ' in the hour%s %s' % (p ,', '.join([str(i) for i in hrs]))

        mins = to_array(self.minutes)
        if not mins:
            result += ' at the top of the hour'
        elif len(mins) > 1:
            result += ' at these minutes: %s' % ', '.join([str(i) for i in mins])
        else:
            result += ' at this minute: %s' % mins[0]
        return result

    def day_number_to_name(self, number):
        if number == 0: return 'Monday'
        if number == 1: return 'Tuesday'
        if number == 2: return 'Wednesday'
        if number == 3: return 'Thursday'
        if number == 4: return 'Friday'
        if number == 5: return 'Saturday'
        if number == 6: return 'Sunday'
        return 'Unknown'

    def due_for_execution(self, timestamp=None, window_minutes=10):
        """Returns True if this event should be run now or using the timestamp if it is not None."""
        if not self.active: return False
        if not timestamp: timestamp = datetime.datetime.utcnow()
        last_time = self.latest_scheduled_time(timestamp)
        if not last_time: return False
        if self.last_run and self.last_run.replace(tzinfo=None) > last_time: return False
        return (timestamp > last_time) and ((timestamp - last_time) < datetime.timedelta(minutes=window_minutes))

    def current_time(self):
        """Returns the current day, hour, and minute"""
        timestamp = datetime.datetime.utcnow()
        print 'timestamp', timestamp
        return 'day:%s hour:%s minute:%s' % (timestamp.weekday(), timestamp.hour, timestamp.minute)

    def save(self, *args, **kwargs):
        self.days = clean_int_field(self.days)
        self.hours = clean_int_field(self.hours)
        self.minutes = clean_int_field(self.minutes)
        super(EventModel, self).save(*args, **kwargs)

    def to_arrays(self):
        """Returns a tuple of python arrays like so: ([days], [hours], [minutes])"""
        return (to_array(self.days), to_array(self.hours), to_array(self.minutes))

    def latest_scheduled_time(self, timestamp=None):
        """Returns a datetime for this event's scheduled time most close to but before the current time or timestamp if it's not None"""
        if not timestamp: timestamp = datetime.datetime.utcnow()
        days, hours, minutes = self.to_arrays()

        if not days and not hours and not minutes: return None

        if not days: days = range(0,7)
        if not hours: hours = range(0,24)
        if not minutes: minutes = [0]

        if timestamp.weekday() in days:
            hour, minute = previous_hour_and_min(timestamp.hour, timestamp.minute, hours, minutes)
            result = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, hour, minute)
            if result < timestamp: return result
        target_day = previous_element(timestamp.weekday(), days)
        result = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, hours[len(hours) - 1], minutes[len(minutes) - 1])
        if timestamp.weekday() < target_day:
            day_diff = -1 * (7 - (target_day - timestamp.weekday()))
        else:
            day_diff = -1 * (timestamp.weekday() - target_day)
        return result + datetime.timedelta(days=day_diff)
    class Meta:
        abstract = True

def previous_hour_and_min(target_hour, target_minute, hours, minutes):
    if target_hour in hours:
        if target_minute in minutes: return (target_hour, target_minute)
        return (target_hour, previous_element(target_minute, minutes))
    if target_minute in minutes: return (previous_element(target_hour, hours), target_minute)
    return (previous_element(target_hour, hours), previous_element(target_minute, minutes))

def previous_element(target, options):
    if len(options) == 1: return options[0]
    for i in range(0, len(options)):
        if options[i] >= target:
            if i == 0: return options[len(options) - 1]
            return options[i - 1]
    return options[len(options) - 1]

def clean_int_field(field_string):
    """Returns a field string, removing duplicates and sorting by ascending order"""
    if not field_string: return field_string
    a = to_array(field_string)
    a.sort()
    cleaned = [str(i) for i in list(set(a))]
    return ','.join(cleaned)

def to_array(field_string):
    """Returns an array from the field string, or [0] if it is None"""
    if not field_string: return None
    return [int(i) for i in field_string.split(',')]
