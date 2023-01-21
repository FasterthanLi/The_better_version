import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
from celery import Celery
from django.core.mail import send_mail

app = Celery('django_project', broker='pyamqp://guest@localhost//')

@app.task
def send_email_task(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)