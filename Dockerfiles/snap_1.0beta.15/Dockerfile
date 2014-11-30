# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Installing MAKE and G++
RUN sudo apt-get update && sudo apt-get install -y make g++

# Installing ZLIB 1.2.8
ADD http://zlib.net/zlib-1.2.8.tar.gz /
RUN sudo tar -xf /zlib-1.2.8.tar.gz
RUN sudo rm /zlib-1.2.8.tar.gz
RUN sudo mv /zlib-1.2.8 /usr/local
RUN sudo ln -s /usr/local/zlib-1.2.8 /usr/local/zlib
RUN cd /usr/local/zlib-1.2.8 && sudo ./configure && sudo make && sudo make install

# Installing SNAP 1.0beta.15
ADD http://snap.cs.berkeley.edu/downloads/snap-1.0beta.15-linux.tar.gz /
RUN sudo tar -zxf /snap-1.0beta.15-linux.tar.gz
RUN sudo rm /snap-1.0beta.15-linux.tar.gz
RUN sudo mv /snap-1.0beta.15-linux /usr/local
RUN sudo ln -s /usr/local/snap-1.0beta.15-linux /usr/local/snap
ENV SNAP_HOME /usr/local/snap

# Adding the home directory to system variable to make SNAP run easier
ENV PATH $PATH:$SNAP_HOME

# Autostarting SNAP to show available commands
RUN bash -c 'echo "snap" >> ~/.bashrc'