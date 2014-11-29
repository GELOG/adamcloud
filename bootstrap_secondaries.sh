#!/bin/bash

#Choosing an IP or Hostname to peer to for Weave
echo "Please enter the IP or Hostname of the primary node."
read input_hostname

#Asking if it's the first (1), second (2), ... secondary node on the cluster
echo "Please enter the rank number. Example, enter 1 if it's the first secondary node on the cluster."
read input_number
if [ "$input_number" -lt 1 ] || [ "$input_number" -gt 8 ]; then
	echo "Invalid number ($input_number). Must be between 1 and 8."
else
	echo "Number ($input_number) is valid."
	
	#Running cAdvisor with web interface on port 8079
	docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:rw --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --publish=8079:8080 --detach=true --name=cadvisor google/cadvisor:latest
	
	#Launching Weave
	sudo weave launch $input_hostname

	#Running the Spark Worker with web interface on port 8081
	sudo weave run 192.168.0.1$input_number/24 -ti --name worker$input_number-spark -h worker$input_number-spark -p 8081:8081 spark_1.1.0-prebuilthadoop2.3 /usr/local/spark/bin/spark-class org.apache.spark.deploy.worker.Worker --ip 192.168.0.1$input_number spark://192.168.0.9:7077

	#Running the HDFS DataNode with web interface on port 50075
	sudo weave run 192.168.0.2$input_number/24 -ti --name datanode$input_number-hdfs -h datanode$input_number-hdfs -p 50075:50075 hadoop_2.3.0
	docker exec datanode$input_number-hdfs mkdir /usr/local/hadoop-2.3.0/logs
	docker exec datanode$input_number-hdfs /usr/local/hadoop/sbin/hadoop-daemon.sh start datanode
fi