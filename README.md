## Flask App Project
Blueprint for Flask App Project
###### Note: python3.7+

#### System dependencies
```
$ sudo apt install libpq-dev
```

#### Python configuration

##### Python Environment
```
$ mkvirtualenv --python=/usr/bin/python3.7 flask_project
$ workon flask_project
```

##### Install requirements
```
$ pip install -r requirements/base.txt
```

#### Configure database (PostgreSQL)

##### Create the postgres role
```
$ sudo -u postgres psql -c "create role flask_app_user with login password 'flask_app_user';"
$ sudo -u postgres psql -c "alter user flask_app_user with superuser;"
```

##### Create the database
```
$ sudo -u postgres createdb flask_project -O flask_app_user
$ sudo -u postgres createdb flask_project_test -O flask_app_user
```

##### Execute tests
```
$ python manage.py test
```

##### Test coverage
```
$ python manage.py coverage
```

##### After the coverage execution you should see some report like that:
```
Coverage summary:

Name                                        Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------------------------------
project/app.py                                 12      5      2      0    64%
project/apps/__init__.py                        2      0      0      0   100%
project/apps/core/__init__.py                   0      0      0      0   100%
project/apps/core/commons/__init__.py           0      0      0      0   100%
project/apps/core/commons/mixins.py             6      0      0      0   100%
project/apps/frontend/__init__.py               1      0      0      0   100%
project/apps/frontend/tests/__init__.py         0      0      0      0   100%
project/apps/frontend/tests/test_views.py       5      0      0      0   100%
project/apps/frontend/views.py                  5      0      0      0   100%
-----------------------------------------------------------------------------
TOTAL                                          31      5      2      0    85%
```

###### Also a folder called: "htmlcov" was created and you can open the index.html file in your browser and see the code lines that our test are covering...

##### Load and stress test using Locust
Locust is an easy-to-use, distributed, user load testing tool. It is intended for load-testing web sites (or other systems) and figuring out how many concurrent users a system can handle.
https://docs.locust.io/en/stable/writing-a-locustfile.html
```
$ locust --port 8090
```

The idea is that during a test, a swarm of locusts will attack your website. The behavior of each locust (or test user if you will) is defined by you and the swarming process is monitored from a web UI in real-time. This will help you battle test and identify bottlenecks in your code before letting real users in.

![LOCUST](assets/locus/locus1.png)

You can see statistics, charts, failures, exceptions...

![LOCUST](assets/locus/locus2.png)

```
Console results...

 Name                             # reqs      # fails     Avg     Min     Max  |  Median   req/s failures/s
-----------------------------------------------------------------------------------------------------------------------
 GET /products/                   14146     0(0.00%)      14       5     101  |      13  345.56    0.00
-----------------------------------------------------------------------------------------------------------------------
 Aggregated                       14146     0(0.00%)      14       5     101  |      13  345.56    0.00

Percentage of the requests completed within given times
 Name                             # reqs    50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100%
-----------------------------------------------------------------------------------------------------------------------
 GET /products/                   14146     13     14     15     16     18     20     24     29     40     65    100
-----------------------------------------------------------------------------------------------------------------------
 Aggregated                       14146     13     14     15     16     18     20     24     29     40     65    100
```

##### Execute the application...
```
$ python manage.py run
```

#### Docker

##### Build the Docker image
```
$ sudo docker-compose up --build --no-recreate

After that, you can go to http://localhost:5000, you will 
see the application up and running.

Then you can list yours images...
$ docker images

REPOSITORY                                TAG                 IMAGE ID            CREATED              SIZE
gcr.io/gcp-platform-test-x/flask-app   latest              39c1f4cd7579        About a minute ago   240MB

Or yours containers...
$ docker ps -a

CONTAINER ID        IMAGE                                            COMMAND                  CREATED              STATUS                        PORTS               NAMES
2c1a336c6fc1        gcr.io/gcp-platform-test-x/flask-app:latest   "flask run --host=0.…"   About a minute ago   Exited (137) 56 seconds ago                       flask-app
```

##### Push the Docker image to the register
```
First, you need to be autenticated in DockerHub...
$ docker login

Then...
docker push 
```

#### Google Cloud Platform

##### Set your GCP configuration
```
$ gcloud config set project [PROJECT_ID] (gcp-platform-test-x)
$ gcloud config set compute/zone [COMPUTE_ENGINE_ZONE] (us-west1-a for example)
```

##### Create the Docker image
```
$ sudo docker build -t gcr.io/[PROJECT_ID]/flask-app .
For this case: sudo docker build -t gcr.io/gcp-platform-test-x/flask-app .
```

##### Login to GCP
```
$ gcloud auth login
```

##### Enable the Container Registry API.
https://cloud.google.com/container-registry/docs/quickstart

##### Configure docker to use the gcloud command-line tool as a credential helper
```
$ gcloud auth configure-docker
```

##### Push the image to Google Container Registry
```
$ docker push gcr.io/gcp-platform-test-x/flask-app
```

##### Deploying the containerized web application...
```
$ gcloud container clusters create gcp-cluster --num-nodes=2
```

It may take several minutes for the cluster to be created. 
Once the command has completed, run the following command and see 
the cluster's two worker VM instances:
```
Creating cluster gcp-cluster in us-west1-a... Cluster is being health-checked (master is healthy)...done.                                                                                                                                                                                                            
Created [https://container.googleapis.com/v1/projects/gcp-platform-test-x/zones/us-west1-a/clusters/gcp-cluster].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/us-west1-a/gcp-cluster?project=gcp-platform-test-x
kubeconfig entry generated for gcp-cluster.

NAME         LOCATION    MASTER_VERSION  MASTER_IP     MACHINE_TYPE   NODE_VERSION    NUM_NODES  STATUS
gcp-cluster  us-west1-a  1.13.11-gke.14  34.83.193.82  n1-standard-1  1.13.11-gke.14  2          RUNNING
```

```
$ gcloud compute instances list

NAME                                        ZONE        MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP    STATUS
gke-gcp-cluster-default-pool-8d83bbad-3s26  us-west1-a  n1-standard-1               10.138.0.2   34.82.112.95   RUNNING
gke-gcp-cluster-default-pool-8d83bbad-w56r  us-west1-a  n1-standard-1               10.138.0.3   35.247.116.96  RUNNING
```

```
$ kubectl create deployment gcp-cluster --image=gcr.io/gcp-platform-test-x/flask-app
```

To see the Pod created by the Deployment, run the following command:
```
$ kubectl get pods

NAME                           READY   STATUS              RESTARTS   AGE
gcp-cluster-66d67f565b-nv6pd   0/1     ContainerCreating   0          12s
```

##### Expose the application
```
$ kubectl expose deployment gcp-cluster --type=LoadBalancer --port 80 --target-port 8080
```

```
$ kubectl get service

NAME          TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
gcp-cluster   LoadBalancer   10.23.252.31   35.247.59.8   80:30793/TCP   70s
```

#### Scale up your application
```
$ kubectl scale deployment gcp-cluster --replicas=3
```

##### Delete your cluster
```
$ gcloud container clusters delete gcp-cluster
```
