# Building the image using my Oracle JDK 7
FROM oraclejdk_7

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Getting SPARK 1.1.0 binaries pre-built for HADOOP 2.3
ADD http://d3kbcqa49mib13.cloudfront.net/spark-1.1.0-bin-hadoop2.3.tgz /
RUN sudo tar -zxf /spark-1.1.0-bin-hadoop2.3.tgz
RUN sudo rm /spark-1.1.0-bin-hadoop2.3.tgz
RUN sudo mv /spark-1.1.0-bin-hadoop2.3 /usr/local
RUN sudo ln -s /usr/local/spark-1.1.0-bin-hadoop2.3 /usr/local/spark
ENV SPARK_HOME /usr/local/spark

# Creating aliases to make SPARK run easier
RUN bash -c 'echo "alias spark-submit="${SPARK_HOME}/bin/spark-submit"" >> ~/.bashrc'
RUN bash -c 'echo "alias spark-shell="${SPARK_HOME}/bin/spark-shell"" >> ~/.bashrc'

# Autostarting SPARK to show available commands
RUN bash -c 'echo "spark-submit" >> ~/.bashrc'