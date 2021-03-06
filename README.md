AdamCloud
=========

[![Join the chat at https://gitter.im/GELOG/adamcloud](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/GELOG/adamcloud?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Description
This repository provides multiple Dockerfiles and Scripts related to the AdamCloud project.

## Available Dockerfiles
* adam : ADAM latest version with Spark 1.1.0 pre-built for Hadoop 2.3
* adam_0.14.0 : ADAM 0.14.0 version with Spark 1.1.0 pre-built for Hadoop 2.3
* avocado : AVOCADO latest version with Spark 1.1.0 pre-built for Hadoop 2.3
* emboss_6.6.0 : EMBOSS 6.6.0 version
* hadoop_2.3.0 : HADOOP 2.3.0 version (useful especially for HDFS in this project)
* oraclejdk_7 : Oracle JDK 7 version (hadoop_2.3.0 and spark_1.1.0-prebuilthadoop2.3 depend on it)
* snap-adam-avocado-spark : SNAP, ADAM and AVOCADO latest versions with Spark 1.1.0 pre-built for Hadoop 2.3
* snap : SNAP latest version
* snap_1.0beta.15 : SNAP 1.0beta.15 version
* spark_1.1.0-prebuilthadoop2.3 : Spark 1.1.0 pre-built for Hadoop 2.3
* spark_1.1.0-source : Spark 1.1.0 from source code
* spark_cdh5 : Spark from CDH 5 (shipping inside)

## Available Scripts
### Local Distributed Environment
* singlehost_images.sh : Pulls cAdvisor, Ubuntu and builds a client (including Snap, Adam and Avocado), OracleJdk, Spark and Hadoop image on the single host
* singlehost_containers.sh : Runs cAdvisor, a client, a Spark Master and a Spark Worker on the single host

### Cluster Environment
* multihosts_pri_images.sh : Pulls cAdvisor, Weave, Ubuntu and builds a Snap, Adam, Avocado, OracleJdk, Spark and Hadoop image for the primary host
* multihosts_sec_images.sh : Pulls cAdvisor, Weave, Ubuntu and builds a OracleJdk, Spark and Hadoop image on a secondary host
* multihosts_pri_containers.sh : Runs cAdvisor, Weave, the clients (Snap, Adam and Avocado), a Spark Master, a HDFS NameNode and a HDFS SecondaryNameNode on the primary host
* multihosts_sec_containers.sh : Runs cAdvisor, Weave, a Spark Worker and a HDFS DataNode on a secondary host

## Tutorial
### Docker basics
To install the latest Docker for Windows, refer to this link: https://docs.docker.com/installation/windows/. Boot2Docker is actually a very small virtual machine (based on Tiny Core Linux distribution) running completely in RAM. Using Boot2Docker in production seems rather premature for the moment and it's more appropriate to use Docker on Linux instead.

To install the latest Docker package for Ubuntu (version 1.0.1 for now), run the following command:
```
sudo apt-get update && sudo apt-get install -y docker.io
```

To install the latest Docker release for Ubuntu (version 1.3.1 for now), run the following commands:
```
sudo sh -c "echo deb https://get.docker.com/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
sudo apt-get update && sudo apt-get install -y --force-yes lxc-docker
```

To build an image from a Dockerfile, run the following command where the Dockerfile is located:
```
sudo docker build -t IMAGE .
```

To run a simple container from an image, run the following command:
```
sudo docker run -ti --name NAME IMAGE
```
*Note: Docker will check if an image with the name NAME is present in the local repository. If so, it creates a container with this image. If not, it downloads the image on Docker Hub and then creates the container.*

If you want to have a shared folder (volume) with the host, create it and then mount it during the run of a container. For example:
```
sudo mkdir /docker-volume
```
```
sudo docker run -ti --name NAME -v /docker-volume:/docker-volume IMAGE
```

## Data for testing
I use the hg19 (GRCh37) reference sequence of the "1000 Genomes" project.
* Details of the reference: http://www.1000genomes.org/faq/which-reference-assembly-do-you-use
* File location: ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/human_g1k_v37.fasta.gz
* Other references: http://hgdownload.cse.ucsc.edu/downloads.html

## Useful commands
### Linux (Ubuntu)
|Command|Description
|---|---
|sudo apt-get install -y *PACKAGE*|Install a package assuming yes to all the questions
|time *COMMAND*|Show execution time of a command
|ls -lh *DIRECTORY*|List in a human readable way details of files in a directory
|rm *FILE*|Remove a file
|rm -r *DIRECTORY*|Remove a directory
|df|Show available space on file systems
|gzip -d *FILE*|Decompress a GNU zip file
|w3m *URL*|Show a web page
|find . -name *FILE*|Find a file with a certain name
|sudo adduser *USER*|Add a new user
|gpasswd -a *USER* sudo|Give root privileges to a user

### Docker
|Command|Description
|---|---
|docker images|Show all local images
|docker ps –a|Show all containers
|docker rmi -f $(docker images -q)|Delete all local images
|docker rm -f $(docker ps –a -q)|Delete all containers
|docker start *CONTAINER*|Start a container
|docker stop *CONTAINER*|Stop a container
|docker attach *CONTAINER*|Attach to a started container
|docker login|Connect to Docker Hub
|docker push *IMAGE*|Push an image to Docker Hub

### HDFS
|Command|Description
|---|---
|hadoop fs -ls hdfs://*IP*:9000/|List details of files in HDFS
|hadoop fs -put *FILE* hdfs://*IP*:9000/|Copy a file from local file system to HDFS
|hadoop fs -get  hdfs://*IP*:9000/*FILE* *FILE*|Copy a file from HDFS to local file system

## Contributors
* Sébastien Bonami (PFE, sep. 2014 - dec. 2014)

