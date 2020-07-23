import os
from flask import Flask, request
import time

from rq import Queue
from redis import Redis

import rq_dashboard
import numpy as np

# Import tasks
from tasks import emptyTask, slowTask, runFinalTask

# Get environment stuff (Should use container environmetn variables)
from environment import env

# Initialized flask app
app = Flask(__name__)

## It should be able to get the dashboard integrated to the flask app, but I can't figure out how :(
# app.config.from_object(rq_dashboard.default_settings)
# app.register_blueprint(rq_dashboard.blueprint, redis_url='redis://' + env['redis']['address'] + ':6379', url_prefix='/rq')

# connect to redis and create queue
redis_conn = Redis(host=env['redis']['address'], port=6379, db=0)
q = Queue('rq-server', connection=redis_conn)

# Just say hi
@app.route('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}

# Run a single task
@app.route('/single', methods = ['POST'])
def singleTask():
    content = request.get_json()
    job = q.enqueue(slowTask,content['time'])
    time.sleep(content['time']+1)
    
    return {'results': 'Finished single task: ' + str(job.result), 'jobID': job.id}, 201

# run a sequence of tasks (first task-> lots of sub jobs -> final task)
@app.route('/sequence', methods = ['POST'])
def sequentialTasks():
    content = request.get_json()
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
    return {'results': 'sequential tasks are running'}, 201

if __name__ == '__main__':
	app.run(
        debug=True, 
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 8080)),
    )