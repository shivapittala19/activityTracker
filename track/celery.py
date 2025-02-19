# track/celery.py

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'activityTracker.settings')

app = Celery('track')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-daily-activities-every-midnight': {
        'task': 'track.tasks.generate_daily_activities',
        'schedule': crontab(hour=0, minute=0),  # Runs at 12:00 AM Everyday
    },
}
