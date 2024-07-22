from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    main = models.CharField(max_length=50)
    temp = models.FloatField()
    feels_like = models.FloatField()
    dt = models.DateTimeField()
    
    def __str__(self):
        return f'{self.city} - {self.main} - {self.temp}°C'
