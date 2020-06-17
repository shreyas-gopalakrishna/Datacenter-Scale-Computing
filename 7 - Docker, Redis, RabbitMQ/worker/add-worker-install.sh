#!/bin/sh

WORKER=$(curl http://metadata/computeMetadata/v1/instance/attributes/worker -H "Metadata-Flavor: Google")
echo "$WORKER" > worker.py

# sudo python3 worker.py