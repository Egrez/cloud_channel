from django.contrib import admin
from .models import Sensor, ServerData, SensorReading

# Register your models here.
admin.site.register(Sensor)
admin.site.register(SensorReading)
admin.site.register(ServerData)