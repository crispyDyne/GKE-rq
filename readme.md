# GKE-rq
Loosely based on this article https://medium.com/@mike.p.moritz/using-docker-compose-to-deploy-a-lightweight-python-rest-api-with-a-job-queue-37e6072a209b

Assumes you already have a GKE project up and running and gcloud tools installed.

Deployment Sequence 
- Create Redis server
    - run createRedis.py
- Set Redis IP in containers (this should be improved)
    - Set "redisIP" in the following locations 
        - dashDockerFile "redis://redisIP:6379"
        - followerDockerFile "redis://redisIP:6379"
        - environment.py "redis://redisIP:6379"
- Build Containers 
    - cd into "cloudBuild" folder
    - run "gcloud builds submit"
- Create Cluster
    - run createCluster.py
    - This should return:
        - Node info, including the [nodeExternalIP]
        - [LeaderPort]
        - [DashPort]

Now make the workers work!
- To run a single job, post a message to your nodes [externalIP]:[LeaderPort]/single
- To run a sequence of jobs, post a message to your  [nodeExternalIP]:[LeaderPort]/sequence
- Open [nodeExternalIP]:[DashPort] in a browser to see the jobs queue up and run.