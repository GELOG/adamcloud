# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Installing Oracke JDK 7
RUN sudo apt-get update && sudo apt-get install -y software-properties-common
RUN sudo add-apt-repository ppa:webupd8team/java -y
RUN sudo apt-get update && sudo echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && sudo apt-get install -y oracle-java7-installer

# Getting SPARK 1.1.0 binaries pre-built for HADOOP 2.3
ADD http://d3kbcqa49mib13.cloudfront.net/spark-1.1.0-bin-hadoop2.3.tgz /
RUN sudo tar -zxf /spark-1.1.0-bin-hadoop2.3.tgz
RUN sudo rm /spark-1.1.0-bin-hadoop2.3.tgz
RUN sudo mv /spark-1.1.0-bin-hadoop2.3 /usr/local
RUN sudo ln -s /usr/local/spark-1.1.0-bin-hadoop2.3 /usr/local/spark
ENV SPARK_HOME /usr/local/spark

# Creating aliases to make SPARK run easier
RUN bash -c 'echo "alias spark-submit="${SPARK_HOME}/bin/spark-submit"" >> ~/.bashrc'
RUN bash -c 'echo "alias spark-shell="${SPARK_HOME}/bin/spark-shell"" >> ~/.bashrc'

# Autostarting SPARK to show available commands
RUN bash -c 'echo "spark-submit" >> ~/.bashrc'