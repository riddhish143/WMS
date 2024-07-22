from apscheduler.schedulers.background import BackgroundScheduler
from weather.fetch_weather import fetch_and_store

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store, 'interval', minutes=5)
    scheduler.start()
