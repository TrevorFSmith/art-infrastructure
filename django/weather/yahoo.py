import urllib2
import urllib
import simplejson

class YahooWeatherClient(object):
	'''
	A util class for reaching the Yahoo Weather API
	https://developer.yahoo.com/weather/
	'''
	API_ROOT = 'https://query.yahooapis.com/v1/public/yql?'

	FORCAST_FORMAT = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")'

	def test(self):
		return self.query_forecast('paris, FRANCE')

	def query_forecast(self, location_name):
		'''
		Find the current conditions and forecast for a place name like 'Paris, France' or 'Seattle, WA'
		'''
		return self.get_json(YahooWeatherClient.FORCAST_FORMAT % location_name)

	def get_json(self, yql_query):
		yql_url = YahooWeatherClient.API_ROOT + urllib.urlencode({'q':yql_query}) + '&format=json'
		data = urllib2.urlopen(yql_url).read()
		return simplejson.loads(data)['query']['results']['channel']

