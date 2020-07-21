from rq import Queue
from redis import Redis
from rq_task import emptyTask, slowTask, runFinalTask
import time
import numpy as np


# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

tasks = np.linspace(0,3,3)

firstTask = q.enqueue(slowTask, 0.5) 
sequenceTask = firstTask
jobs = []
jobIDs = []
for t in tasks:
    job = q.enqueue(slowTask, t, depends_on = firstTask)
    jobs.append(job)
    jobIDs.append(job.id)

sequenceTasks = []
for j in jobs:
    sequenceTasks.append( q.enqueue(runFinalTask, jobIDs, depends_on = j) )


# lastTask = q.enqueue(slowTask, 0.9, depends_on = sequenceTask) 

# Now, wait a while, until the worker is finished
lastTaskID = False
while True:
    time.sleep(0.5)
    print("first: " + (firstTask.result if firstTask.result else "None"))   # => 889

    for j in jobs:
        print("job: " + (j.result if j.result else "None"))   # => 889

    for s in sequenceTasks:
        if s.result:
            print("sequence: " + s.result)   # => 889
            lastTaskID = s.result if len(s.result) > 20 else False
        else:
            print("sequence: none") 

    if lastTaskID:
        lastTask = q.fetch_job(lastTaskID)
        print("last: " + (lastTask.result if lastTask.result else "None"))   # => 889
