# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Installing Oracle JDK 7
RUN sudo apt-get update && sudo apt-get install -y software-properties-common
RUN sudo add-apt-repository ppa:webupd8team/java -y
RUN sudo apt-get update && sudo echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && sudo apt-get install -y oracle-java7-installer
RUN ln -s /usr/lib/jvm/java-7-oracle /usr/lib/jvm/jdk
ENV JAVA_HOME /usr/lib/jvm/jdk