## CSCI 5253 - Data Center Scale Computing - Project

Scalable Service for Character Recognition and Content Categorization


### Team Members
Joon il Kwon

Shreyas Gopalakrishna

#### Project URL
https://github.com/cu-csci-4253-datacenter-fall-2019/final-project-repository-shreyas-g-ucb


#### Project Goals
Character recognition - A web service takes images of documents or notes, performs OCR (Optical character recognition) on them and stores the input image and the converted text.

Content classification - The contents of documents are analyzed with keywords to classify them into specific topics. Users can view documents based on the categories.

Search based on Keywords - A search feature to search a word across all uploaded documents
Scalable service - The service is designed to scale to accommodate increased workloads as multiple users try to access the service.


#### Components
Kubernetes

Google Vision API

Google Natural Language API

Google Cloud Storage (Bucket)

Redis

REST Server

CloudSQL

RabbitMQ

### Steps to Run code
1. `gcloud container clusters create mykube` creates a kubernetes cluster.
2. `sh redis-launch.sh` creates docker image of redis, pushes it to kubernetes, and exposes port.
3. `sh rabbitmq-launch.sh` creates docker image of rabbitmq, pushes it to kubernetes, and exposes port.
4. `sh cloudsql-create.sh` creates cloud sql instance and sets the permissions and password.
5. `sh rest-launch.sh` creates docker image with flask and other modules installed, pushes it to kubernetes, and exposes 5000 port for REST API.
6. `sh worker-launch.sh` creates docker image for worker with required modules installed, pushes it to kubernetes and waits for messages from rabbitmq.
7. `sh logs-launch.sh` creates docker image for logswith required modules installed, pushes it to kubernetes and waits for debug messages from rest and worker.
8. `sh frontend-launch.sh` creates docker image of httpd,adds the frontend code base, pushes it to kubernetes, and exposes port 80 for website access.

##### Note
DCSC.json is the GOOGLE_APPLICATION_CREDENTIALS file. It is not included in the repository.

A custom service credentials json from must be generated and used to run the project.


##### UI Template Credits
https://github.com/ColorlibHQ/AdminLTE/releases/tag/v2.4.18



#### Sources
https://cloud.google.com/vision/docs/ocr

https://cloud.google.com/vision/docs/auth

https://medium.com/@jdegange85/document-image-datasets-b7f8df01010d

https://cloud.google.com/natural-language/docs/classify-text-tutorial

Code snippets from previous lab assignments


*-Shreyas Gopalakrishna*

*-Joon il Kwon*

