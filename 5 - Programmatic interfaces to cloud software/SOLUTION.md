## CSCI 5253 - Data Center Scale Computing - Lab 5

### Part 1
-  Created a VM
-  Added firewall
- Installed the flask tutorial application

Command to run script: `python create_instance.py dcsc-2 dcsc-bucket --zone us-west1-b --name dcsc-instance`
provide - project, bucket, zone and instance name

- added firewall using `compute.firewalls().insert(project=project, body=firewall_body)`
- set the network tag using ` compute.instances().setTags(project=project, zone=zone, instance=instance_name, body=tags_body)`

Instance with flask installed was created and count be accessed using extrenal IP.
Example: [35.230.38.32:5000](http://35.230.38.32:5000 "35.230.38.32:5000")

### Part 2 
-  Created snapshot of instance
-  Created 3 instances using the snapshot and measured time.
- Flask running on all 3 instances

Command to run script: `python create_snapshot.py`

Snapshot created using `compute.instances().insert(project=project,zone=zone,body=config).execute()`
Instances created by providing snapshot info in `sourceSnapshot`

Stored time taken to create instance in `TIMING.md`

### Part 3
- Created service account key
- Used it to create VM and pass script which creates another VM to run flask

Command to run script: `python lab-5-part-3.py dcsc-2 dcsc-bucket --zone us-west1-b --name dcsc-instance-part-3`
Python script, start script and service account info passed using `metadata`

### Sources
- https://cloud.google.com/compute/docs/reference/rest/v1/firewalls/insert
- https://cloud.google.com/compute/docs/reference/rest/v1/instances
- https://cloud.google.com/compute/docs/reference/rest/v1/disks/createSnapshot
- https://cloud.google.com/iam/docs/understanding-service-accounts


*-Shreyas Gopalakrishna*

