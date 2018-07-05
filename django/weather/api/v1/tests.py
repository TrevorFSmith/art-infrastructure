from django.core.urlresolvers import reverse
from ai.factories import *
from rest_framework.test import APITestCase
import json


class WeatherUnregisteredEndpointTestCase(APITestCase):

    def test_get_200_for_unregistered_user(self):
        location = LocationFactory()
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': location.gps_code}))
        self.assertEqual(response.status_code, 200)

    def test_get_404_for_unregistered_user(self):
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': "none"}))
        self.assertEqual(response.status_code, 404)

    def test_get_weather_for_unregistered_user(self):
        location = LocationFactory()
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': location.gps_code}))
        response_content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)

        all_keys = ["id", "condition", "temperature", "atmosphere_pressure", "atmosphere_rising", "atmosphere_visibility", 
                    "atmosphere_humidity", "wind_direction", "wind_speed", "wind_chill", "created"]
        response_all_keys = response_content.keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))
