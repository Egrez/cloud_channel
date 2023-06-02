from django.shortcuts import render
from sensors.models import Sensor, SensorReading, ServerData

# Create your views here.
def home(request):
    sensors = Sensor.objects.all()
    sensor_readings = SensorReading.objects.all()
    server_data = ServerData.objects.all()
    locations = Sensor.objects.values_list('location', flat=True).distinct()

    return render(request, "index.html", { 'sensors': sensors, 'sensor_readings': sensor_readings, 
                                          'server_data': server_data, 'locations': locations })