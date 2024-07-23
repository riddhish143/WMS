from django.test import TestCase, Client
from django.core.mail import outbox
from django.utils import timezone
from unittest.mock import patch
from weather.models import WeatherData
from weather.fetch_weather import kelvin_to_celsius, store_weather_data, fetch_weather, check_alerts

class WeatherDataTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.api_response = {
            'name': 'Delhi',
            'weather': [{'main': 'Clear'}],
            'main': {'temp': 300, 'feels_like': 298},
            'dt': 1618317040
        }

    def test_kelvin_to_celsius(self):
        self.assertEqual(round(kelvin_to_celsius(273.15), 2), 0)
        self.assertEqual(round(kelvin_to_celsius(300), 2), 26.85)

    @patch('weather.fetch_weather.fetch_weather', return_value={
        'name': 'Delhi',
        'weather': [{'main': 'Clear'}],
        'main': {'temp': 300, 'feels_like': 298},
        'dt': 1618317040
    })
    
    def test_store_weather_data(self, mock_fetch_weather):
        store_weather_data(self.api_response)
        weather_data = WeatherData.objects.get(city='Delhi')
        self.assertEqual(weather_data.temp, kelvin_to_celsius(300))
        self.assertEqual(weather_data.feels_like, kelvin_to_celsius(298))

    @patch('weather.fetch_weather.fetch_weather', return_value={
        'name': 'Delhi',
        'weather': [{'main': 'Clear'}],
        'main': {'temp': 300, 'feels_like': 298},
        'dt': 1618317040
    })
    
    def test_fetch_weather(self, mock_fetch_weather):
        data = fetch_weather('Delhi')
        self.assertEqual(data['name'], 'Delhi')
        self.assertEqual(data['main']['temp'], 300)

    # def test_daily_summary(self):
    #     WeatherData.objects.create(
    #         city='Delhi',
    #         main='Clear',
    #         temp=26.85,
    #         feels_like=25.85,
    #         dt=timezone.now()
    #     )
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Delhi')
    #     self.assertContains(response, 'Clear')
    #     self.assertContains(response, '26.85')

    # @patch('weather.fetch_weather.fetch_weather', return_value={
    #     'name': 'Delhi',
    #     'weather': [{'main': 'Clear'}],
    #     'main': {'temp': 300, 'feels_like': 298},
    #     'dt': 1618317040
    # })
    # def test_check_alerts(self, mock_fetch_weather):
    #     WeatherData.objects.create(
    #         city='Delhi',
    #         main='Clear',
    #         temp=36,
    #         feels_like=35,
    #         dt=timezone.now()
    #     )
    #     check_alerts(WeatherData.objects.last())
    #     self.assertEqual(len(outbox), 1)
    #     self.assertIn('High temperature detected in Delhi', outbox[0].subject)

if __name__ == '__main__':
    TestCase.main()
