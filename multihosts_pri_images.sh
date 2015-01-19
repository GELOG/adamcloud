#!/bin/bash

#Pulling and building Docker images
docker pull google/cadvisor
docker pull zettio/weave
docker pull ubuntu:14.04
docker build --rm=true -t snap Dockerfiles/snap
docker build --rm=true -t adam Dockerfiles/adam
docker build --rm=true -t avocado Dockerfiles/avocado
docker build --rm=true -t oraclejdk_7 Dockerfiles/oraclejdk_7
docker build --rm=true -t spark_1.1.0-prebuilthadoop2.3 Dockerfiles/spark_1.1.0-prebuilthadoop2.3
docker build --rm=true -t hadoop_2.3.0 Dockerfiles/hadoop_2.3.0