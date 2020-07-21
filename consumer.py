import sys
import os
import django
import time
import datetime
#django.setup()
#settings.configure()

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()


from kafka import KafkaConsumer
from restapi.models import Event
import json

if __name__ == "__main__":
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',auto_offset_reset='latest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    consumer.subscribe(['event-analytics'])
        #print('consumer')
    for m in consumer:
        data1 = json.loads(m.value)
        format = "%d/%m/%Y"
        date_str = data1['timestamp']
        d = datetime.datetime.strptime(date_str,"%d/%m/%Y %H:%M:%S")
        timestamp = d.timestamp()
        #timestamp = datetime.datetime(date).timestamp()
        message = data1['message']
        event_type = data1['event_type']
        e = Event(event_type = event_type, timestamp = timestamp, message = message)
        e.save()