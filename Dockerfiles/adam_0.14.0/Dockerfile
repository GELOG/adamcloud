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

# Installing JDK
RUN sudo apt-get update && sudo apt-get install -y default-jdk

# Getting MAVEN 3.2.3
ADD http://mirror.its.dal.ca/apache/maven/maven-3/3.2.3/binaries/apache-maven-3.2.3-bin.tar.gz /
RUN sudo tar -zxf /apache-maven-3.2.3-bin.tar.gz
RUN sudo rm /apache-maven-3.2.3-bin.tar.gz
RUN sudo mv /apache-maven-3.2.3 /usr/local
RUN sudo ln -s /usr/local/apache-maven-3.2.3/bin/mvn /usr/bin/mvn

# Giving more memory for MAVEN
ENV MAVEN_OPTS -Xmx512m -XX:MaxPermSize=128m

# Installing ADAM 0.14.0
ADD https://github.com/bigdatagenomics/adam/archive/adam-parent-0.14.0.tar.gz /
RUN sudo tar -zxf /adam-parent-0.14.0.tar.gz
RUN sudo rm /adam-parent-0.14.0.tar.gz
RUN sudo mv /adam-adam-parent-0.14.0 /usr/local
RUN sudo ln -s /usr/local/adam-adam-parent-0.14.0 /usr/local/adam
RUN sed -i /usr/local/adam/pom.xml -e '27s!2.2!2.3!'
RUN cd /usr/local/adam && sudo mvn clean package -DskipTests
ENV ADAM_HOME /usr/local/adam

# Creating aliases to make ADAM run easier
RUN bash -c 'echo "alias adam-submit="${ADAM_HOME}/bin/adam-submit"" >> ~/.bashrc'
RUN bash -c 'echo "alias adam-shell="${ADAM_HOME}/bin/adam-shell"" >> ~/.bashrc'

# Autostarting ADAM to show available commands
RUN bash -c 'echo "adam-submit" >> ~/.bashrc'