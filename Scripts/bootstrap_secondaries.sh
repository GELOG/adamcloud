#!/bin/bash

#Running cAdvisor with web interface on port 8079
sudo docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:rw --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --publish=8079:8080 --detach=true --name=cadvisor google/cadvisor:latest

#Building Docker images
sudo docker build -t oraclejdk_7 Dockerfiles/oraclejdk_7
sudo docker build -t spark_1.1.0-prebuilthadoop2.3 Dockerfiles/spark_1.1.0-prebuilthadoop2.3
sudo docker build -t hdfs Dockerfiles/hdfs

#Launching Weave by choosing a IP/Hostname to peer to
echo "Please enter the IP/Hostname of the primary node:"
read input_hostname
sudo weave launch $input_hostname

#Asking which number...
echo "Please enter the number...:"
read input_number

#Running the Spark Worker with web interface on port 8081
sudo weave run 10.0.1.$input_number/24 -ti --name "worker$input_number" -p 8081:8081 --expose 1000$input_number --net=host -v /docker-volume:/docker-volume spark_1.1.0-prebuilthadoop2.3 /usr/local/spark/bin/spark-class org.apache.spark.deploy.worker.Worker -p 1000$input_number spark://10.0.1.9:7077