from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_type', 'timestamp', 'message']

class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = []