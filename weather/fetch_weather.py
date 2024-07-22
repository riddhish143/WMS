import requests
from datetime import datetime
from django.conf import settings
from weather.models import WeatherData
from django.core.mail import send_mail

API_KEY = '703e4d89be452ed5374b861cff0f88e7'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def fetch_weather(city):
    params = {'q': city, 'appid': API_KEY}
    response = requests.get(BASE_URL.format(city, API_KEY), params=params)
    return response.json()

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def store_weather_data(data):
    weather_entry = WeatherData.objects.create(
        city=data['name'],
        main=data['weather'][0]['main'],
        temp=kelvin_to_celsius(data['main']['temp']),
        feels_like=kelvin_to_celsius(data['main']['feels_like']),
        dt=datetime.fromtimestamp(data['dt'])
    )
    
    check_alerts(weather_entry)

def check_alerts(weather_entry):
    threshold_temp = 35
    recent_records = WeatherData.objects.filter(city=weather_entry.city).order_by('-dt')[:2]
    
    if len(recent_records) >= 2:
        if all(rec.temp > threshold_temp for rec in recent_records):
            send_alert(weather_entry.city, recent_records[0].temp)

def send_alert(city, temp):
    send_mail(
        'Weather Alert',
        f'Alert: High temperature detected in {city} - {temp}°C',
        'riddhishmahajan6822@gmail.com',
        ['riddhishmahajan143@gmail.com'],
    )

def fetch_and_store():
    for city in CITIES:
        data = fetch_weather(city)
        if data['cod'] != '404':
            store_weather_data(data)
          
