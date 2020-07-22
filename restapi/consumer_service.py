import datetime

from kafka import KafkaConsumer
from rest_framework.utils import json
import logging

from restapi.models import Event

logger = logging.getLogger(__name__)

class ConsumerService:

    @classmethod
    def start_consumer(cls, args=None):
        logger.info('Starting consumer service..')
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092', auto_offset_reset='latest',
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        consumer.subscribe(['event-analytics'])
        print('consumer')
        for m in consumer:
            data1 = json.loads(m.value)
            date_str = data1['timestamp']
            d = datetime.datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
            timestamp = d.timestamp()
            message = data1['message']
            event_type = data1['event_type']
            e = Event(event_type=event_type, timestamp=timestamp, message=message)
            e.save()
            print(e)