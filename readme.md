# GKE-rq
Loosely based on this article https://medium.com/@mike.p.moritz/using-docker-compose-to-deploy-a-lightweight-python-rest-api-with-a-job-queue-37e6072a209b

Assumes you already have a GKE project up and running and gcloud tools installed.

Deployment Sequence 
- run createRedis.py
- Set redis IP in the following locations 
-- dashDockerFile "redis://<redisIP>:6379"
-- followerDockerFile "redis://<redisIP>:6379"
-- environment.py "redis://<redisIP>:6379"
- Build Containers "gcloud builds submit"
- run createCluster.py