from celery.schedules import crontab
import os

CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]

CELERY_IMPORTS = ('app.functions')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'Europe/Prague'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'app.functions.refresh_offer_prices',
        # Every minute
        'schedule': crontab()
    }
}