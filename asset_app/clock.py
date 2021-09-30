from apscheduler.schedulers.blocking import BlockingScheduler
from tools import smsAutoLateReturn, smsAutoReturnReminder, smsAutoLoanAsset

TINYMCE_DEFAULT_CONFIG = {
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,",# plugins,
    "toolbar": "styleselect |undo redo | bold italic | alignleft aligncenter alignright | link image media codesample code", # toolbar
    "height": 500,  # texteditor height

}

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



sched.start()