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
            'items': []
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]


def createIntsanceAndAddFirewall(service,project,zone,instance_name,bucket,snapshot):
    operation = create_instance(service, project, zone, instance_name, bucket, snapshot)
    wait_for_operation(service, project, zone, operation['name'])

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
    return response["networkInterfaces"][0]["networkIP"]


credentials = GoogleCredentials.get_application_default()

service = discovery.build('compute', 'v1', credentials=credentials)

# Project ID for this request.
project = 'dcsc-2'  # TODO: Update placeholder value.

# The name of the zone for this request.
zone = 'us-west1-a'  # TODO: Update placeholder value.
dzone = 'europe-west3-a'
bucket = 'dcsc-bucket'

# Creating instance from snapshot

snapshot_name = 'snapshot-2'

url = createIntsanceAndAddFirewall(service,project,zone,'local',bucket,snapshot_name)
print("Local: " + url)

url = createIntsanceAndAddFirewall(service,project,zone,'same-zone',bucket,snapshot_name)
print("Same-Zone: " + url)

url = createIntsanceAndAddFirewall(service,project,dzone,'different-zone',bucket,snapshot_name)
print("Different-zone: " + url)