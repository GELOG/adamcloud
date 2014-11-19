# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Installing Oracke JDK 7
RUN sudo apt-get update && sudo apt-get install -y software-properties-common
RUN sudo add-apt-repository ppa:webupd8team/java -y
RUN sudo apt-get update && sudo echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && sudo apt-get install -y oracle-java7-installer

# Installing SBT 0.13.6
ADD http://apt.typesafe.com/repo-deb-build-0002.deb /
RUN sudo dpkg -i /repo-deb-build-0002.deb
RUN sudo rm /repo-deb-build-0002.deb
RUN sudo apt-get update && sudo apt-get install -y sbt
ADD http://dl.bintray.com/sbt/debian/sbt-0.13.6.deb /
RUN sudo dpkg -i /sbt-0.13.6.deb
RUN sudo rm /sbt-0.13.6.deb

# Installing SCALA 2.10.4
ADD http://www.scala-lang.org/files/archive/scala-2.10.4.tgz /
RUN sudo tar -zxf /scala-2.10.4.tgz
RUN sudo rm /scala-2.10.4.tgz
RUN sudo mv /scala-2.10.4 /usr/local
RUN sudo ln -s /usr/local/scala-2.10.4 /usr/local/scala
ENV SCALA_HOME /usr/local/scala

# Installing SPARK 1.1.0
ADD http://d3kbcqa49mib13.cloudfront.net/spark-1.1.0.tgz /
RUN sudo tar -zxf /spark-1.1.0.tgz
RUN sudo rm /spark-1.1.0.tgz
RUN sudo mv /spark-1.1.0 /usr/local
RUN sudo ln -s /usr/local/spark-1.1.0 /usr/local/spark
RUN cd /usr/local/spark && sudo sbt/sbt assembly
ENV SPARK_HOME /usr/local/spark

# Creating aliases to make SPARK run easier
RUN bash -c 'echo "alias spark-submit="${SPARK_HOME}/bin/spark-submit"" >> ~/.bashrc'
RUN bash -c 'echo "alias spark-shell="${SPARK_HOME}/bin/spark-shell"" >> ~/.bashrc'

# Autostarting SPARK to show available commands
RUN bash -c 'echo "spark-submit" >> ~/.bashrc'
