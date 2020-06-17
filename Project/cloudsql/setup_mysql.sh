# MySQL Creation
gcloud config set project dclab5-254517 # Set your own project id
# https://cloud.google.com/sql/docs/mysql/create-instance
gcloud sql instances create mysql-test --database-version=MYSQL_5_7 --region=us-west1 --storage-type=HDD --storage-size=10GB 

# Setup mysql user/password
gcloud sql users set-password root --host='%' --instance=mysql-test --password=csci5253

# Setup Google Could sql proxy use: NOT accessible directly with MySQL instance name
# https://cloud.google.com/sql/docs/mysql/quickstart-proxy-test
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances=dclab5-254517:us-west1:mysql-test=tcp:3306

# Python-MySQL Connector Library
sudo pip3 install mysql-connector-python

# Connect mysql console
gcloud sql connect mysql --user root

# Sample Commands
# SHOW DATABASES;
# CREATE database ocr-db;
# USE ocr-db;
# DROP DATABASE to_be_deleted_db;

# DOCKERS: Test Purposes
# https://hub.docker.com/_/mysql
# docker run --name mysql -e MYSQL_ROOT_PASSWORD=csci5253 -d mysql:5.7
# docker logs mysql
# docker exec -it mysql bash

# MYSQL CREATION RESULTS
#dc2019f@cloudshell:~/project/mysql (dclab5-254517)$ gcloud sql instances create mysql-test --database-version=MYSQL_5_7 
#--region=us-west1 --storage-type=HDD --storage-size=10GB                                                                
#Creating Cloud SQL instance...⠶
#Creating Cloud SQL instance...done.
#Created [https://www.googleapis.com/sql/v1beta4/projects/dclab5-254517/instances/mysql-test].
#NAME        DATABASE_VERSION  LOCATION    TIER              PRIMARY_ADDRESS  PRIVATE_ADDRESS  STATUS
#mysql-test  MYSQL_5_7         us-west1-a  db-n1-standard-1  34.82.164.225    -                RUNNABLE
