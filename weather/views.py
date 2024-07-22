from django.shortcuts import render
from weather.models import WeatherData
import pandas as pd

def daily_summary():
    weather_records = WeatherData.objects.all().values()
    df = pd.DataFrame(weather_records)
    df['dt'] = pd.to_datetime(df['dt'])
    df.set_index('dt', inplace=True)
    
    summary = df.resample('D').agg({
        'temp': ['mean', 'max', 'min'],
        'main': lambda x: x.value_counts().idxmax()
    })
    
    summary.columns = ['avg_temp', 'max_temp', 'min_temp', 'dominant_weather']
    summary.reset_index(inplace=True)
    return summary.to_dict(orient='records')

def index(request):
    summary = daily_summary()
    return render(request, 'weather/index.html', {'summary': summary})


def daily_weather_summaries(request):
    summaries = daily_summary()  # Assuming this returns a list of daily summaries
    return render(request, 'weather/daily_summaries.html', {'summaries': summaries})

def historical_trends():
    weather_records = WeatherData.objects.all().values()
    df = pd.DataFrame(weather_records)
    df['dt'] = pd.to_datetime(df['dt'])
    df.set_index('dt', inplace=True)
    
    # Example: Monthly average temperature
    monthly_trends = df.resample('M').agg({'temp': 'mean'})
    return monthly_trends.to_dict(orient='records')

def view_historical_trends(request):
    trends = historical_trends()
    return render(request, 'weather/historical_trends.html', {'trends': trends})

# Function for Triggered Alerts
def check_for_alerts():
    alerts = []
    # Example: Check for any day with temp > 30°C
    weather_records = WeatherData.objects.all().values()
    df = pd.DataFrame(weather_records)
    high_temp_days = df[df['temp'] > 30]
    if not high_temp_days.empty:
        alerts.append("High temperature alert!")
    return alerts

# View for Alerts
def view_alerts(request):
    alerts = check_for_alerts()
    return render(request, 'weather/alerts.html', {'alerts': alerts})