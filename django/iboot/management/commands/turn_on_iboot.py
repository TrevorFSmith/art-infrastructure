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

from iboot.iboot_control import IBootControl

class Command(BaseCommand):

    help = "turns on an iboot."

    def add_arguments(self, parser):
        parser.add_argument('ip', nargs=1)
        parser.add_argument('password', nargs=1)

    def handle(self, *labels, **options):
        control = IBootControl(options['password'][0], options['ip'][0])
        print control.turn_on()
