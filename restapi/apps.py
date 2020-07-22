import logging
import sys
from threading import Thread

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class RestapiConfig(AppConfig):
    name = 'restapi'

    def ready(self):
        print(sys.argv)
        if 'runserver' not in sys.argv:
            return True
        logger.info('Starting consumer service..')
        ConsumerThread().start()


class ConsumerThread(Thread):

    def run(self):
        from restapi.consumer_service import ConsumerService
        ConsumerService.start_consumer()


