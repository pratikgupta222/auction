import os
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_site.settings')
 
app = Celery('auction_site')
app.config_from_object('django.conf:settings')
 
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
 
# app.conf.beat_schedule = {
#     'send-report-every-single-minute': {
#         'task': 'publisher.tasks.send_view_count_report',
#         'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#     },
# }