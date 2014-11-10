# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Installing MAKE and G++
RUN sudo apt-get update && sudo apt-get install -y make g++

# Installing ZLIB 1.2.8
RUN ADD http://zlib.net/zlib-1.2.8.tar.gz /
RUN sudo tar -zxf /zlib-1.2.8.tar.gz
RUN sudo rm /zlib-1.2.8.tar.gz
RUN sudo mv /zlib-1.2.8 /usr/local
RUN sudo ln -s /usr/local/zlib-1.2.8 /usr/local/zlib
RUN cd /usr/local/zlib-1.2.8 && sudo ./configure && sudo make && sudo make install

# Installing SNAP 1.0beta.15
ADD http://snap.cs.berkeley.edu/downloads/snap-1.0beta.15-linux.tar.gz /
RUN sudo tar -zxf /snap-1.0beta.15-linux.tar.gz
RUN sudo rm /snap-1.0beta.15-linux.tar.gz
RUN sudo ln -s /snap-1.0beta.15-linux /snap
RUN cd /snap && sudo make

# Creating an alias to make SNAP run easier
RUN bash -c 'echo "alias snap="/snap/snap"" >> /.bashrc'

# Autostarting SNAP to show available commands
RUN bash -c 'echo "snap" >> /.bashrc'