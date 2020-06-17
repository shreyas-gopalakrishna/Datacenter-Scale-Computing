# RabbitMQ Messaging

You should create a server that provides a RabbitMQ message server. The instance name should be `rabbitmq` so that worker nodes can use DNS names to locate the instance. You should provide a startup script `rabbitmq-install.sh` that installs rabbitmq and starts the server. There are [directions on starting RabbitMQ](https://computingforgeeks.com/how-to-install-latest-rabbitmq-server-on-ubuntu-18-04-lts/) of how to do this.

Make sure that your instance does not have an external IP address using the `--network-interface=no-address` flag if using the `gcloud` command interface or similar method if using Python.

You must provide a python program or shell script `rabbitmq-launch.sh` that then starts an instance and also launches the `rabbitmq-install.sh` script.

You do not need to create any queues or exchanges; this will be done by the worker and rest VM's.

# *N.B.*

If you restart or delete your rabbitmq instance, any messages (e.g. outstanding images that need to be processed) in the instance will not be retained. This isn't a design flaw in rabbitmq and [there are extensive directions on how to turn this into a reliable service](https://www.rabbitmq.com/admin-guide.html).