#!/bin/bash

PATH_TO_DROP_DF=/tmp/dockerfiles
PATH_SNAP=$PATH_TO_DROP_DF/snap
PATH_JAVA=$PATH_TO_DROP_DF/java
PATH_SPARK=$PATH_TO_DROP_DF/spark
PATH_ADAM=$PATH_TO_DROP_DF/adam
PATH_AVOCADO=$PATH_TO_DROP_DF/avocado

#Pulling and building Docker images
docker pull google/cadvisor
docker pull zettio/weave
docker pull ubuntu:14.04

#This is temporary, until does Dockers files get on a Docker Registry
mkdir -p $PATH_TO_DROP_DF

mkdir -p $PATH_JAVA
wget -O $PATH_JAVA/Dockerfile https://raw.githubusercontent.com/GELOG/docker-ubuntu-java/oraclejdk7/Dockerfile
docker build --rm=true -t java:oraclejdk7 $PATH_JAVA

mkdir -p $PATH_SPARK
wget -O $PATH_SPARK/Dockerfile https://raw.githubusercontent.com/GELOG/docker-ubuntu-spark/master/Dockerfile
docker build --rm=true -t spark:1.1.0-bin-hadoop2.3 $PATH_SPARK

mkdir -p $PATH_SNAP
wget -O $PATH_SNAP/Dockerfile https://raw.githubusercontent.com/GELOG/docker-ubuntu-snap/master/Dockerfile
docker build --rm=true -t snap $PATH_SNAP

mkdir -p $PATH_ADAM
wget -O $PATH_ADAM/Dockerfile https://raw.githubusercontent.com/GELOG/docker-ubuntu-adam/master/Dockerfile
docker build --rm=true -t adam $PATH_ADAM

mkdir -p $PATH_AVOCADO
wget -O $PATH_AVOCADO/Dockerfile https://raw.githubusercontent.com/GELOG/docker-ubuntu-avocado/master/Dockerfile
docker build --rm=true -t avocado $PATH_AVOCADO

