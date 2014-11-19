# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Installing GIT, MAKE and G++
RUN sudo apt-get update && sudo apt-get install -y git make g++

# Installing ZLIB 1.2.8
ADD http://zlib.net/zlib-1.2.8.tar.gz /
RUN sudo tar -xf /zlib-1.2.8.tar.gz
RUN sudo rm /zlib-1.2.8.tar.gz
RUN sudo mv /zlib-1.2.8 /usr/local
RUN sudo ln -s /usr/local/zlib-1.2.8 /usr/local/zlib
RUN cd /usr/local/zlib-1.2.8 && sudo ./configure && sudo make && sudo make install

# Installing SNAP
RUN sudo git clone https://github.com/amplab/snap
RUN sudo mv /snap /usr/local
RUN cd /usr/local/snap && sudo make
ENV SNAP_HOME /usr/local/snap

# Creating an alias to make SNAP run easier
RUN bash -c 'echo "alias snap="${SNAP_HOME}/snap"" >> ~/.bashrc'

# Autostarting SNAP to show available commands
RUN bash -c 'echo "snap" >> ~/.bashrc'