import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hermes.settings')

app = Celery('hermes')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# We used CELERY_BROKER_URL in settings.py instead of:
# app.conf.broker_url = ''

# We used CELERY_BEAT_SCHEDULER in settings.py instead of:
# app.conf.beat_scheduler = ''django_celery_beat.schedulers.DatabaseScheduler'

app.conf.beat_schedule = {
    'send-email-5-minuts': {
        'task': 'send_notification',
        'schedule': crontab(minute='*/5'), #crontab(hour=7, minute=30, day_of_week=1)
        'args': ('Teste celery', 'Huru, deu certo!')
    },
}

#app.conf.timezone = 'UTC'