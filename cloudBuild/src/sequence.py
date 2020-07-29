from rq import Queue
from redis import Redis
from tasks import emptyTask, slowTask, runFinalTask
import time
import numpy as np

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

## Initialization task. Runs before jobs
firstTask = q.enqueue(slowTask, 0.5) 

## Main jobs, run after initialization
times = 1 + 5 * np.random.rand((50))
jobs = []
jobIDs = []
for t in times:
    job = q.enqueue(slowTask, t, depends_on = firstTask)
    jobs.append(job)
    jobIDs.append(job.id)

# sequence tasks check if all jobs are done, if they are, the final task is run. 
sequenceTask = q.enqueue(runFinalTask, jobIDs, depends_on = firstTask)
sequenceTaskID = sequenceTask.id

# Now, watch and wait as the tasks are completed (hopefully in the right order!)
lastTaskID = False
lastTaskResult = None
while lastTaskResult is None: # keep looping until the last task is completed. 
    time.sleep(1)
    print("first: " + str(firstTask.result) )

    for j in jobs:
        print("job: " + str(j.result) )

    sequenceTask = q.fetch_job(sequenceTaskID)
    print("sequence: " + str(sequenceTask.result))
    if sequenceTask.result:
        if not lastTaskResult and all(sequenceTask.result[1]):
            lastTaskID = sequenceTask.result[0]
        if not lastTaskID:
            sequenceTaskID = sequenceTask.result[0]

    if lastTaskID:
        lastTask = q.fetch_job(lastTaskID)
        lastTaskResult = lastTask.result 

    print("last: " + str(lastTaskResult))
