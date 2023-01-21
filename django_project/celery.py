# settings.py
import os
from celery import Celery

# Set up Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
app = Celery('django_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Set up RabbitMQ as the message broker
app.conf.broker_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/')