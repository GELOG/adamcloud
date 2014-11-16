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

# Installing GIT, MAKE, G++ and JDK
RUN sudo apt-get update && sudo apt-get install -y git make g++ default-jdk

# Installing ZLIB 1.2.8 (for SNAP)
ADD http://zlib.net/zlib-1.2.8.tar.gz /
RUN sudo tar -zxf /zlib-1.2.8.tar.gz
RUN sudo rm /zlib-1.2.8.tar.gz
RUN sudo mv /zlib-1.2.8 /usr/local
RUN sudo ln -s /usr/local/zlib-1.2.8 /usr/local/zlib
RUN cd /usr/local/zlib-1.2.8 && sudo ./configure && sudo make && sudo make install

# Installing SNAP
RUN sudo git clone https://github.com/amplab/snap
RUN cd /snap && sudo make

# Getting MAVEN 3.2.3 (for ADAM and AVOCADO)
ADD http://mirror.its.dal.ca/apache/maven/maven-3/3.2.3/binaries/apache-maven-3.2.3-bin.tar.gz /
RUN sudo tar -zxf /apache-maven-3.2.3-bin.tar.gz
RUN sudo rm /apache-maven-3.2.3-bin.tar.gz
RUN sudo mv /apache-maven-3.2.3 /usr/local
RUN sudo ln -s /usr/local/apache-maven-3.2.3/bin/mvn /usr/bin/mvn

# Giving more memory for MAVEN
ENV MAVEN_OPTS -Xmx512m -XX:MaxPermSize=128m

# Installing ADAM
RUN git clone https://github.com/bigdatagenomics/adam
RUN sed -i /adam/pom.xml -e '27s!2.2!2.3!'
RUN cd /adam && sudo mvn clean package -DskipTestexp

# Installing AVOCADO
RUN sudo git clone https://github.com/bigdatagenomics/avocado
RUN cd /avocado && sudo mvn package

# Creating aliases to make SNAP, ADAM and AVOCADO run easier
RUN bash -c 'echo "alias snap="/snap/snap"" >> /.bashrc'
RUN bash -c 'echo "alias adam="/adam/bin/adam-submit"" >> /.bashrc'
RUN bash -c 'echo "alias adam-shell="/adam/bin/adam-shell"" >> /.bashrc'
RUN bash -c 'echo "alias avocado="/avocado/bin/avocado-submit"" >> /.bashrc'