from django.test import TestCase
from weather.models import WeatherData
from weather.fetch_weather import kelvin_to_celsius, store_weather_data

class WeatherDataTests(TestCase):

    def test_kelvin_to_celsius(self):
        self.assertEqual(kelvin_to_celsius(273.15), 0)

    def test_store_weather_data(self):
        data = {
            'name': 'Delhi',
            'weather': [{'main': 'Clear'}],
            'main': {'temp': 300, 'feels_like': 298},
            'dt': 1618317040
        }
        store_weather_data(data)
        self.assertEqual(WeatherData.objects.count(), 1)
