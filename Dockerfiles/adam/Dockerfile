# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Getting SPARK 1.1.0 binaries pre-built for HADOOP 2.3
ADD http://d3kbcqa49mib13.cloudfront.net/spark-1.1.0-bin-hadoop2.3.tgz /
RUN sudo tar -zxf /spark-1.1.0-bin-hadoop2.3.tgz
RUN sudo rm /spark-1.1.0-bin-hadoop2.3.tgz
RUN sudo mv /spark-1.1.0-bin-hadoop2.3 /usr/local
RUN sudo ln -s /usr/local/spark-1.1.0-bin-hadoop2.3 /usr/local/spark
ENV SPARK_HOME /usr/local/spark

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

# Installing ADAM
RUN git clone https://github.com/bigdatagenomics/adam
RUN sudo mv /adam /usr/local
RUN sed -i /usr/local/adam/pom.xml -e '27s!2.2!2.3!'
RUN cd /usr/local/adam && sudo mvn clean package -DskipTestexp
ENV ADAM_HOME /usr/local/adam

# Adding the home directory to system variable to make ADAM run easier
ENV PATH $PATH:$ADAM_HOME/bin

# Autostarting ADAM to show available commands
RUN bash -c 'echo "adam-submit" >> ~/.bashrc'