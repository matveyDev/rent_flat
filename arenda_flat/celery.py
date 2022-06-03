import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arenda_flat.settings')

app = Celery('arenda_flat')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-notificationsails': {
        'task': 'celerytasks.tasks.send_notifications',
        #Каждые 30 минут
        'schedule': 30 * 60,
    }
}