#!/bin/bash

#Running cAdvisor with web interface on port 8079
sudo docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:rw --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --publish=8079:8080 --detach=true --name=cadvisor google/cadvisor:latest

#Building Docker images
sudo docker build -t snap-adam-avocado-spark Dockerfiles/snap-adam-avocado-spark
sudo docker build -t oraclejdk_7 Dockerfiles/oraclejdk_7
sudo docker build -t spark_1.1.0-prebuilthadoop2.3 Dockerfiles/spark_1.1.0-prebuilthadoop2.3
sudo docker build -t hdfs hdfs

#Lauching Weave
sudo weave launch

#Running the client (SNAP, ADAM and AVOCADO with SPARK)
sudo weave run 10.0.1.10/24 -ti --name "client" --net=host -v /docker-volume:/docker-volume snap-adam-avocado-spark

#Running the Spark Master with web interface on port 8080
sudo weave run 10.0.1.9/24 -ti --name "master" -p 8080:8080 --net=host -v /docker-volume:/docker-volume spark_1.1.0-prebuilthadoop2.3 /usr/local/spark/bin/spark-class org.apache.spark.deploy.master.Master

#Running the HDFS NameNode with web interface on port 50070
#sudo weave run 10.0.1.11/24 -ti --name "namenode" -p 50070:50070 -v /docker-volume:/docker-volume hadoop_2.3.0
#sudo docker exec namenode service ssh start