# Redis database

You should create a container that provides a Redis database and provided a service called `redis` so that worker nodes can use DNS names to locate the instance. Feel free to build your own container image [or use the one provided by the Redis developers](https://hub.docker.com/_/redis).

You don't need to create any database tables in advance -- that happens automatically when you start using the database; see instructions in `worker/README-worker.md`.

You must create a script `redis-launch.sh` that creates the deployment and service. When you create the redis service, you'll need to expose port 6379. Unlike the lab using virtual machines, you won't need to need to change the configuration file.

# *N.B.*

If you delete your redis pod, the database will also be deleted because we didn't provide a volume for the data. If you want to avoid that problem, you can create [a kubernetes Persistent Volume and Persistent Volume claim](https://cloud.google.com/kubernetes-engine/docs/concepts/persistent-volumes).

We're not using Redis because it's great, we're using it because it's easy, so if you don't want to do this, don't bother.