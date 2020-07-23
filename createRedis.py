import subprocess
import json

# Redis Settings
redisName = 'test-server'
redisSize = '1'

## Redis server
# create redis server
createRedisServer = subprocess.run(['gcloud', 'redis', 'instances', 'create', redisName, '--size', redisSize, 
    '--region', 'us-central1', '--redis-version', 'redis_5_0'])

# get redis server ip (needed later)
redisServerDetails = subprocess.run(['gcloud', 'redis', 'instances', 'describe', redisName,
    '--region', 'us-central1', '--format', 'json'], capture_output=True)
redisServerDetails = json.loads(redisServerDetails.stdout)
redisServerIP = redisServerDetails['host']
print(redisServerIP)
