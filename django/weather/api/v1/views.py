from rest_framework.views import APIView
from weather import serializers, models
from django.http import Http404
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from weather.yahoo import YahooWeatherClient


class WeatherViewSet(APIView):

    def get(self, request, airport_code, format=None):
        location = models.Location.objects.search(airport_code)
        if location is None:
            raise Http404

        weather_info = models.WeatherInfo.objects.filter(location=location, created__gt=timezone.now() - timedelta(hours=1)).first()
        if weather_info is None:
            models.WeatherInfo.objects.all().filter(location=location).delete()
            yahoo_data = YahooWeatherClient().query_forecast(location.municipality_and_country)
            weather_info = models.WeatherInfo.objects.create(
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
        serializer = serializers.WeatherInfoSerializer(weather_info)
        return Response(serializer.data)
