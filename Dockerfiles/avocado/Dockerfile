# Building the image using UBUNTU
FROM ubuntu:latest

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Getting SPARK 1.0.0 binaries pre-built for HADOOP 2.2
ADD http://d3kbcqa49mib13.cloudfront.net/spark-1.0.1-bin-hadoop2.tgz /
RUN sudo tar -zxf /spark-1.0.1-bin-hadoop2.tgz
RUN sudo rm /spark-1.0.1-bin-hadoop2.tgz
RUN sudo mv /spark-1.0.1-bin-hadoop2 /usr/local
ENV SPARK_HOME /usr/local/spark-1.0.1-bin-hadoop2

# Installing GIT and JDK
RUN sudo apt-get update && sudo apt-get install -y git default-jdk

# Getting MAVEN 3.2.3
ADD http://mirror.its.dal.ca/apache/maven/maven-3/3.2.3/binaries/apache-maven-3.2.3-bin.tar.gz /
RUN sudo tar -zxf /apache-maven-3.2.3-bin.tar.gz
RUN sudo rm /apache-maven-3.2.3-bin.tar.gz
RUN sudo mv /apache-maven-3.2.3 /usr/local
RUN sudo ln -s /usr/local/apache-maven-3.2.3/bin/mvn /usr/bin/mvn

# Giving more memory for MAVEN
ENV MAVEN_OPTS -Xmx512m -XX:MaxPermSize=128m

# Installing AVOCADO
RUN sudo git clone https://github.com/bigdatagenomics/avocado
RUN cd /avocado && sudo mvn package

# Creating an alias to make AVOCADO run easier
RUN bash -c 'echo "alias avocado="/avocado/bin/avocado-submit"" >> /.bashrc'

# Autostarting AVOCADO to show available commands
RUN bash -c 'echo "avocado" >> /.bashrc'