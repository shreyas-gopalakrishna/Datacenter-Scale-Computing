from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import argparse
import os
import time

import googleapiclient.discovery
from six.moves import input

# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]

# [START create_instance]
def create_instance(compute, project, zone, name, bucket, snapshot):
    # Get the latest Debian Jessie image.
    
    source_snapshot = snapshot

    # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup-script-lab-2.sh'), 'r').read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceSnapshot': 'global/snapshots/' + source_snapshot,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],
        "tags": {
            "items": [
            "allow-5000"
            ]
        },

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }, {
                'key': 'url',
                'value': image_url
            }, {
                'key': 'text',
                'value': image_caption
            }, {
                'key': 'bucket',
                'value': bucket
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]


def createIntsanceAndAddFirewall(service,project,zone,instance_name,bucket,snapshot):
    start_time = time.time()
    operation = create_instance(service, project, zone, instance_name, bucket, snapshot)
    wait_for_operation(service, project, zone, operation['name'])
    ctime = time.time() - start_time

    request = service.instances().get(project=project, zone=zone, instance=instance_name)
    response = request.execute()
    tags_body = {
        "items": [
    "allow-5000"
    ]}
    tags_body["fingerprint"] = response["tags"]["fingerprint"]
    request = service.instances().setTags(project=project, zone=zone, instance=instance_name, body=tags_body)
    response = request.execute()

    # get ip:
    request = service.instances().get(project=project, zone=zone, instance=instance_name)
    response = request.execute()
    return "Flask running - http://" + response["networkInterfaces"][0]["accessConfigs"][0]["natIP"] + ":5000", ctime


credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)

# Project ID for this request.
project = 'dcsc-2'  # TODO: Update placeholder value.

# The name of the zone for this request.
zone = 'us-west1-b'  # TODO: Update placeholder value.

bucket = 'dcsc-bucket' 

# Instance name
instance = 'dcsc-instance'

request = service.disks().list(project=project, zone=zone)
diskInfo = None
while request is not None:
    response = request.execute()

    for disk in response['items']:
        # TODO: Change code below to process each `disk` resource:
        # pprint(disk)
        diskInfo = disk

    request = service.disks().list_next(previous_request=request, previous_response=response)


# Name of the persistent disk to snapshot.
disk = diskInfo['name']  # TODO: Update placeholder value.
print(disk)
snapshot_body = {}
snapshot_body["name"] = "base-snapshot-" + instance

request = service.disks().createSnapshot(project=project, zone=zone, disk=disk, body=snapshot_body)
response = request.execute()

wait_for_operation(service, project, zone, response['name'])

# # TODO: Change code below to process the `response` dict:
# pprint(response)

# Creating 3 instance from snapshot

instance_name = 'instance-from-snapshot-'

output = ""
for i in range(0,3):
    url,ctime = createIntsanceAndAddFirewall(service,project,zone,instance_name+str(i+1),bucket,snapshot_body["name"])
    output += "Instance " + str(i+1) + " - " + str(ctime) + " seconds\n"
    print(url)

# write to a file
with open('TIMING.md','w') as f:
	f.write(output)