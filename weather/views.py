import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render
from weather.models import WeatherData
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from weather.fetch_weather import fetch_and_store

fetch_and_store()

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
    summaries = daily_summary() 
    return render(request, 'weather/daily_summaries.html', {'summary': summaries})

def historical_trends():
    weather_records = WeatherData.objects.all().values()
    df = pd.DataFrame(weather_records)
    df['dt'] = pd.to_datetime(df['dt'])
    df.set_index('dt', inplace=True)
    monthly_trends = df.resample('M').agg({'temp': 'mean'})
    return monthly_trends.to_dict(orient='records')

def view_historical_trends(request):
    trends = historical_trends()
    return render(request, 'weather/historical_trends.html', {'trends': trends})

def check_for_alerts():
    alerts = []
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

def generate_plots():
    weather_records = WeatherData.objects.all().values()
    df = pd.DataFrame(weather_records)
    df['dt'] = pd.to_datetime(df['dt'])
    df.set_index('dt', inplace=True)

    # Ensure the directory exists
    static_dir = os.path.join('weather', 'static', 'weather')
    os.makedirs(static_dir, exist_ok=True)

    # Daily Summary Plot
    daily_summary = df.resample('D').agg({
        'temp': ['mean', 'max', 'min'],
        'main': lambda x: x.value_counts().idxmax()
    })
    daily_summary.columns = ['avg_temp', 'max_temp', 'min_temp', 'dominant_weather']
    daily_summary.reset_index(inplace=True)

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=daily_summary, x='dt', y='avg_temp', label='Average Temperature')
    sns.lineplot(data=daily_summary, x='dt', y='max_temp', label='Max Temperature')
    sns.lineplot(data=daily_summary, x='dt', y='min_temp', label='Min Temperature')
    plt.title('Daily Temperature Summary')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.xticks(rotation=45)
    daily_plot_path = os.path.join(static_dir, 'daily_summary.png')
    plt.savefig(daily_plot_path)
    plt.close()

    # # Monthly Trends Plot
    # monthly_trends = df.resample('M').agg({'temp': 'mean'})
    # plt.figure(figsize=(10, 6))
    # sns.lineplot(data=monthly_trends, x=monthly_trends.index, y='temp')
    # plt.title('Monthly Temperature Trends')
    # plt.xlabel('Month')
    # plt.ylabel('Average Temperature (°C)')
    # plt.xticks(rotation=45)
    # monthly_plot_path = os.path.join(static_dir, 'monthly_trends.png')
    # plt.savefig(monthly_plot_path)
    # plt.close()

def view_plots(request):
    generate_plots()
    return render(request, 'weather/plot.html')