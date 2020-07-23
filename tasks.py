from rq import Queue
from redis import Redis

import random
import time

from environment import env

# Tell RQ what Redis connection to use
redis_conn = Redis(host=env['redis']['address'], port=6379, db=0)
q = Queue('rq-server', connection=redis_conn)

def emptyTask():
    return True

def slowTask(sleepTime): 
    time.sleep(sleepTime)
    return str(sleepTime)

def runFinalTask(job_IDs):
    # get the status of all jobs
    finished = []
    for job_id in job_IDs:
        job = q.fetch_job(job_id)
        finished.append(job.result)


    if all(finished): # if all jobs are finished, run the final task
        finalTask = q.enqueue(slowTask, 3) 
    else: # otherwise keep waiting...
        time.sleep(2) # Short delay before trying again
        finalTask = q.enqueue(runFinalTask, job_IDs)

    return [finalTask.id,finished]