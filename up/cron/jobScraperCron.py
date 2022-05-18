from crontab import CronTab

JOB_SCRAPER_ID = 'CRON_JOB_SCRAPER'


def createJobScraperCron():
    with CronTab(user=True) as cron:
        if not cron.find_comment(JOB_SCRAPER_ID):
            job = cron.new(command='echo hello_world', comment=JOB_SCRAPER_ID)
            job.minute.every(1)
            cron.write()

if __name__ == '__main__':
    print('Creating job scraper cron')
    createJobScraperCron()
