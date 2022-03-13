from django.contrib import admin
from django.urls import path, include
from .views import Twitch

urlpatterns = [
    path('twitch/', Twitch.as_view(), name='twitch')
]
