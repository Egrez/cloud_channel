from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('sensor', views.sensor, name='sensor'),
    path('warn/<int:id>', views.send_warning_signal, name='warn'),
    path('signin', views.signin, name='signin'),
]
