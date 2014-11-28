#!/bin/bash

#Building Docker images
sudo docker build --rm=true -t snap Dockerfiles/snap
sudo docker build --rm=true -t adam Dockerfiles/adam
sudo docker build --rm=true -t avocado Dockerfiles/avocado
sudo docker build --rm=true -t oraclejdk_7 Dockerfiles/oraclejdk_7
sudo docker build --rm=true -t spark_1.1.0-prebuilthadoop2.3 Dockerfiles/spark_1.1.0-prebuilthadoop2.3
sudo docker build --rm=true -t hadoop_2.3.0 Dockerfiles/hadoop_2.3.0

#Running cAdvisor with web interface on port 8079
sudo docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:rw --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --publish=8079:8080 --detach=true --name=cadvisor google/cadvisor:latest

#Lauching Weave
sudo weave launch

#Running the clients (SNAP, ADAM and AVOCADO)
sudo weave run 192.168.0.1/24 -ti --name client-snap -h client-snap snap
sudo weave run 192.168.0.2/24 -e SPARK_LOCAL_IP=192.168.0.2 -ti --name client-adam -h client-adam adam
sudo weave run 192.168.0.3/24 -e SPARK_LOCAL_IP=192.168.0.3 -ti --name client-avocado -h client-avocado avocado

#Running the Spark Master with web interface on port 8080
sudo weave run 192.168.0.9/24 -ti --name master-spark -h master-spark -p 8080:8080 spark_1.1.0-prebuilthadoop2.3 /usr/local/spark/bin/spark-class org.apache.spark.deploy.master.Master --ip 192.168.0.9

#Running the HDFS NameNode with web interface on port 50070
sudo weave run 192.168.0.19/24 -ti --name namenode-hdfs -h namenode-hdfs -p 50070:50070 -v /docker-volume:/docker-volume hadoop_2.3.0
sudo docker exec namenode-hdfs hdfs namenode -format
sudo docker exec namenode-hdfs mkdir /usr/local/hadoop-2.3.0/logs
sudo docker exec namenode-hdfs /usr/local/hadoop/sbin/hadoop-daemon.sh start namenode

#Running the HDFS SecondaryNameNode with web interface on port 50090
sudo weave run 192.168.0.20/24 -ti --name secnamenode-hdfs -h secnamenode-hdfs -p 50090:50090 -v /docker-volume:/docker-volume hadoop_2.3.0
sudo docker exec secnamenode-hdfs mkdir /usr/local/hadoop-2.3.0/logs
sudo docker exec secnamenode-hdfs /usr/local/hadoop/sbin/hadoop-daemon.sh start secondarynamenode