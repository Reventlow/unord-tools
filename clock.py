import django
from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
import UnordToolsProject
from UnordToolsProject import settings

from django.core.exceptions import ImproperlyConfigured
import os
import sys
sys.path.append(
    os.path.join(os.path.dirname(__file__), 'UnordToolsProject')
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UnordToolsProject.settings")

from django.conf import settings
print("django.setup() start")
django.setup()
print("django.setup() complete")
from asset_app.tools import smsAutoLateReturn, smsAutoReturnReminder, smsAutoLoanAsset


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    #test



@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7)
def scheduled_job_everyday_seven_am():
    smsAutoLateReturn()
    smsAutoReturnReminder()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=16)
def scheduled_job_weekdays_four_pm():
    smsAutoLoanAsset()


sched.start()