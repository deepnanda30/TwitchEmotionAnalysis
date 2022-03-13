from email import message
from django.contrib.auth.models import User
from rest_framework import serializers


class TwitchSerializer(serializers.Serializer):
   message = serializers.ListField(child=serializers.CharField())