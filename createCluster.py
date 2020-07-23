
import subprocess
import json

# project settings
projectName = 'yourProjectName' # put your project name here
clusterName = 'rq-test'

# Cluster Settings
machineType = 'n1-standard-2'
numberNodes = '1'

##
subprocess.run(['gcloud', 'beta', 'container', 'clusters', 'create', clusterName, 
    '--release-channel', 'regular',
    '--identity-namespace', projectName + '.svc.id.goog',
    '--machine-type', machineType, '--num-nodes', numberNodes, '--preemptible',
    '--enable-stackdriver-kubernetes', '--enable-ip-alias'
])

subprocess.run(['gcloud', 'container', 'clusters', 'get-credentials', clusterName])

## need to apply the redis server IP to these deployments
# deploy leader
subprocess.run(['kubectl', 'create', 'deployment', 'rq-leader', '--image', 'gcr.io/' + projectName + '/rq-tests-leader:latest'])

# deploy follower
subprocess.run(['kubectl', 'create', 'deployment', 'rq-follower', '--image', 'gcr.io/' + projectName + '/rq-tests-follower:latest'])
subprocess.run(['kubectl', 'autoscale', 'deployment', 'rq-follower', '--max', '8', '--min', '4', '--cpu-percent', '60']) # autoscale the follower. Needs improvement.

# deploy dashboard
subprocess.run(['kubectl', 'create', 'deployment', 'rq-dash', '--image', 'gcr.io/' + projectName + '/rq-tests-dash:latest'])


## Expose Leader Service
# create leader service
leaderServiceDetails = subprocess.run(['kubectl', 'expose', 'deployment', 'rq-leader', '--name', 'rq-leader-service',
 '--type', 'NodePort', '--port', '80', '--target-port', '8080'],
 capture_output=True)

# get leader service details
leaderServiceDetails = subprocess.run(['kubectl','get','services','rq-leader-service','-o','json'], capture_output=True)
leaderServiceDetails = json.loads(leaderServiceDetails.stdout)
leaderServiceNodePort = str(leaderServiceDetails['spec']['ports'][0]['nodePort'])

# open port for leader service
subprocess.run(['gcloud', 'compute', 'firewall-rules', 'create', 'node-port-leader', '--allow', 'tcp:' + leaderServiceNodePort])

## Follower service does not need to be exposed

## Expose Dash Service
# create dash service
subprocess.run(['kubectl', 'expose', 'deployment', 'rq-dash', '--name', 'rq-dash-service',
 '--type', 'NodePort', '--port', '80', '--target-port', '9181'],
 capture_output=True)

# get dash service details
dashServiceDetails = subprocess.run(['kubectl','get','services','rq-dash-service','-o','json'], capture_output=True)
dashServiceDetails = json.loads(dashServiceDetails.stdout)
dashServiceNodePort = str(dashServiceDetails['spec']['ports'][0]['nodePort'])

# open port for dash service
subprocess.run(['gcloud', 'compute', 'firewall-rules', 'create', 'node-port-dash', '--allow', 'tcp:' + dashServiceNodePort])

subprocess.run(['kubectl', 'get', 'nodes', '-o', 'wide']) # display active nodes to get IP
print('Leader Port: ' + leaderServiceNodePort)
print('Dashboard Port: ' + dashServiceNodePort)
