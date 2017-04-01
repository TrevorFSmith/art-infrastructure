import os
import sys
import os
import csv
import time
from datetime import date, timedelta

from django.conf import settings
from django.db import connection
from django.utils import encoding
from django.utils import timezone
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from weather.models import Location

class Command(BaseCommand):
	help = "Imports info from the airports.csv into Location records."
	requires_system_checks = True

	def handle(self, *labels, **options):
		airports_csv_path = os.path.join(settings.BASE_DIR, 'weather', 'airports.csv')
		if not os.path.isfile(airports_csv_path):
			print 'Can not find %s' % airports_csv_path
			return
		airport_reader = csv.reader(open(airports_csv_path))
		count = 0
		Location.objects.all().delete()
		for row in airport_reader:
			Location.objects.create(
				name=row[0],
				airport_type=row[1],
				latitude=parse_float_field(row[2]),
				longitude=parse_float_field(row[3]),
				elevation=parse_float_field(row[4]),
				iso_country=row[5],
				iso_region=row[6],
				municipality=row[7],
				gps_code=row[8],
				iata_code=row[9],
				local_code=row[10]
			)
			count +=1 
			if count % 1000 == 0:
				sys.stdout.write('.')
				sys.stdout.flush()
		sys.stdout.write('\n')

def parse_float_field(val):
	if val == '': return None
	return float(val)
