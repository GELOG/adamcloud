# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

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
RUN sudo ln -s /adam-adam-parent-0.14.0 /adam
# RUN sed -i /adam/pom.xml -e '27s!2.2!2.3!'
RUN cd /adam && sudo mvn clean package -DskipTests

# Creating aliases to make ADAM run easier
RUN bash -c 'echo "alias adam="/adam/bin/adam-submit"" >> /.bashrc'
RUN bash -c 'echo "alias adam-shell="/adam/bin/adam-shell"" >> /.bashrc'

# Autostarting ADAM to show available commands
RUN bash -c 'echo "adam" >> /.bashrc'