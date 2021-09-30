from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    pass

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7)
def scheduled_job_everyday_seven_am():
    pass

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=16)
def scheduled_job_weekdays_four_pm():
    pass



sched.start()