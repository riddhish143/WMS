from django.urls import path
from weather import views

urlpatterns = [
    path('', views.index, name='index'),
    path('daily-summaries/', views.daily_weather_summaries, name='daily_summaries'),
    path('alerts/', views.view_alerts, name='alerts'),
    path('plots/', views.view_plots, name='view_plots'),
]
