import pytz

from datetime import timedelta

from django.http import Http404
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse

from yahoo import YahooWeatherClient

from models import (
	Location,
	WeatherInfo
)

def icao_airport_observation(request, airport_code):
	'''
	This returns the old NOAA style weather data.

	For example, passing in an airport code of 'rjaa' (or 'RJAA') would return something like this:
	New Tokyo Inter-National Airport, Japan (RJAA) 35-46N 140-23E 44M
	Jan 20, 2010 - 01:00 PM EST / 2010.01.20 1800 UTC
	Wind: from the SW (220 degrees) at 22 MPH (19 KT) gusting to 36 MPH (31 KT):0
	Visibility: greater than 7 mile(s):0
	Sky conditions: mostly cloudy
	Temperature: 60 F (16 C)
	Dew Point: 51 F (11 C)
	Relative Humidity: 72%
	Pressure (altimeter): 29.68 in. Hg (1005 hPa)
	ob: RJAA 201800Z 22019G31KT 9999 FEW030 SCT180 BKN/// 16/11 Q1005 NOSIG RMK 1CU030 3AC180 A2970 P/FR
	cycle: 18	
	'''
	location = Location.objects.search(airport_code)
	if location is None: raise Http404

	weather_info = WeatherInfo.objects.filter(location=location, created__gt=timezone.now() - timedelta(hours=1)).first()
	if weather_info is None:
		yahoo_data = YahooWeatherClient().query_forecast(location.municipality_and_country)
		weather_info = WeatherInfo.objects.create(
			location=location,
			condition=yahoo_data['item']['condition']['text'],
			temperature=float(yahoo_data['item']['condition']['temp']),
			atmosphere_pressure=float(yahoo_data['atmosphere']['pressure']),
			atmosphere_rising=float(yahoo_data['atmosphere']['rising']),
			atmosphere_visibility=float(yahoo_data['atmosphere']['visibility']),
			atmosphere_humidity=float(yahoo_data['atmosphere']['humidity']),
			wind_direction=float(yahoo_data['wind']['direction']),
			wind_speed=float(yahoo_data['wind']['speed']),
			wind_chill=float(yahoo_data['wind']['chill'])
		)
	return HttpResponse(generate_noaa_weather(weather_info), content_type='text/plain')

def get_wind_direction(degrees):
	if degrees > 337.5 and degrees <= 22.5: return 'N'
	if degrees > 22.5 and degrees <= 67.5: return 'NE'
	if degrees > 67.5 and degrees <= 112.5: return 'E'
	if degrees > 112.5 and degrees <= 157.5: return 'SE'
	if degrees > 157.5 and degrees <= 202.5: return 'S'
	if degrees > 202.5 and degrees <= 247.5: return 'SW'
	if degrees > 247.5 and degrees <= 292.5: return 'W'
	return 'Northwest'

def f_to_c(fahrenheit_degrees):
	return (fahrenheit_degrees - 32) / (9.0/5.0)

def generate_noaa_weather(weather_info):
	local_tz = timezone.get_current_timezone()
	local_time = local_tz.normalize(weather_info.created.astimezone(local_tz))

	result = []
	result.append('Airport (%s)' % weather_info.location.gps_code)
	result.append(local_time.strftime('%b %d, %Y - %H:%M %p %Z / ') + weather_info.created.strftime('%Y.%m.%d %H%M %Z'))
	if weather_info.wind_speed == 0:
		result.append('Wind: None')
	else:
		result.append('Wind: from the %s (%s degrees) at %s MPH' % (get_wind_direction(weather_info.wind_direction), weather_info.wind_direction, int(weather_info.wind_speed)))
	result.append('Visibility: greater than %s mile(s)' % weather_info.atmosphere_visibility)
	result.append('Sky conditions: %s' % weather_info.condition)
	result.append('Temperature: %s F (%s C)' % (int(weather_info.temperature), int(f_to_c(weather_info.temperature))))
	result.append('Relative Humidity: %s%%' % int(weather_info.atmosphere_humidity))
	return '\n'.join(result) + '\n'
