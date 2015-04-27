#!/bin/bash

#Running cAdvisor with web interface on port 8079
docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:rw --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --publish=8079:8080 --detach=true --name=cadvisor google/cadvisor:latest

#Running the client (SNAP, ADAM and AVOCADO)
docker run -d -ti --name client-genomics -h client-genomics -v /docker-volume:/docker-volume snap-adam-avocado-spark

#Running the Spark Master and Worker with web interfaces on ports 8080 and 8081
docker run -d -ti --name spark -h spark -p 8080:8080 -p 8081:8081 --link client-genomics:client-genomics -v /docker-volume:/docker-volume spark_1.1.0-prebuilthadoop2.3
docker exec -d spark /usr/local/spark/bin/spark-class org.apache.spark.deploy.master.Master
docker exec -d spark /usr/local/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark:7077

#Add hosts entry for Spark IP Address in the client
SPARK_IP=`eval "docker inspect --format '{{ .NetworkSettings.IPAddress }}' spark"`
docker exec client-genomics sudo -- sh -c "echo $SPARK_IP spark >> /etc/hosts"