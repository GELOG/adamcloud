# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Installing WGET
RUN sudo apt-get update && sudo apt-get install -y wget

# Installing Oracke JDK 7
RUN sudo apt-get update && sudo apt-get install -y software-properties-common
RUN sudo add-apt-repository ppa:webupd8team/java -y
RUN sudo apt-get update && sudo echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && sudo apt-get install -y oracle-java7-installer

# Installing CDH 5
ADD http://archive.cloudera.com/cdh5/one-click-install/precise/amd64/cdh5-repository_1.0_all.deb /
RUN dpkg -i cdh5-repository_1.0_all.deb

# Installing SPARK
RUN sudo apt-get update && sudo apt-get install -y spark-core spark-master spark-worker spark-history-server spark-python

# Fixing issue (Reference: https://groups.google.com/a/cloudera.org/forum/#!topic/cdh-user/eAW-hiUHdzY)
ADD https://raw.githubusercontent.com/apache/spark/master/bin/utils.sh /usr/lib/spark/bin