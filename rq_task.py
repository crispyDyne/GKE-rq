from rq import Queue
from redis import Redis

import random
import time

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

def emptyTask():
    return True

def slowTask(sleepTime): 
    time.sleep(sleepTime)
    return str(sleepTime)

def runFinalTask(job_IDs):
    finished = []
    for job_id in job_IDs:
        job = q.fetch_job(job_id)
        finished.append(job.result)

    if all(finished):
        finalTask = q.enqueue(slowTask, 0.9) 
        return finalTask.id
    else:
        return "Keep waiting"
