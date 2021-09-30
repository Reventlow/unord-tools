from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
import UnordToolsProject
from UnordToolsProject import settings
from asset_app.tools import smsAutoLateReturn, smsAutoReturnReminder, smsAutoLoanAsset
from django.core.exceptions import ImproperlyConfigured
import os


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    #test
    smsAutoLoanAsset()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7)
def scheduled_job_everyday_seven_am():
    smsAutoLateReturn()
    smsAutoReturnReminder()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=16)
def scheduled_job_weekdays_four_pm():
    smsAutoLoanAsset()

def configure():
    TINYMCE_DEFAULT_CONFIG = os.environ[UnordToolsProject.settings.TINYMCE_DEFAULT_CONFIG]




sched.start()