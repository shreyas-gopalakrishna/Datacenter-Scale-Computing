# RabbitMQ Messaging

You should create a container that provides a RabbitMQ message server. The container and resulting service name should be `rabbitmq` so that worker nodes can use DNS names to locate the instance. Feel free to build your own container image [or use the one provided by the Rabbitmq developers](https://hub.docker.com/_/rabbitmq).


You must create a script `rabbitmq-launch.sh` that creates the deployment and service. When you create the rabbitmq service, you'll need to expose port 5672. Unlike the lab using virtual machines, you won't need to need to change the configuration file.

You do not need to create any queues or exchanges; this will be done by the worker and rest VM's.

# *N.B.*

If you restart or delete your rabbitmq instance, any messages (e.g. outstanding images that need to be processed) in the instance will not be retained. This isn't a design flaw in rabbitmq and [there are extensive directions on how to turn this into a reliable service](https://www.rabbitmq.com/admin-guide.html).