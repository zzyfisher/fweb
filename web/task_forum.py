#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
使用celery做任务调度
pip3 install celery
pip3 install celery-with-redis
'''
from celery import Celery
from celery.task import task
import time

celery = Celery("app.name", broker='redis://localhost:6379/0')
celery.conf.CELERY_RESULT_BACKEND='redis://localhost:6379/0'

@celery.task(bind=True)
def scan_forum_task(self,id):
    print("***")
    """Background task that runs a long function with progress reports."""

    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)

    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42,
            'id':id}

if __name__=='__main__':	
	result = scan_forum_task.delay(100)
	while not result.ready():
		print ("not ready yet")
		time.sleep(5)
	print( result.get())