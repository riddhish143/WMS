from django.urls import path
from weather import views

urlpatterns = [
    path('', views.index, name='index'),
    path('daily-summaries/', views.daily_weather_summaries, name='daily_summaries'),
    path('historical-trends/', views.view_historical_trends, name='historical_trends'),
    path('alerts/', views.view_alerts, name='alerts'),
]
