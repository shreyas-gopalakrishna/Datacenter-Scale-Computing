#!/bin/sh
gcloud sql instances create mysql --tier=db-n1-standard-2 --region=us-west1-b
gcloud sql users set-password root --host=% --instance mysql --password csci5253