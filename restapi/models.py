from django.db import models
from django_unixdatetimefield import UnixDateTimeField
from enum import Enum

class EventChoice(Enum):   # A subclass of Enum
    BC = "BUTTON_CLICKED"
    LC = "LINK_CLICKED"
    WC = "WINDOW_CLOSED"

# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key = True)
    event_type = models.CharField(max_length = 20, choices=[(tag, tag.value) for tag in EventChoice])
    timestamp = models.IntegerField()
    message = models.CharField(max_length = 100)