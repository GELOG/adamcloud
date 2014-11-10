# Building the image using UBUNTU 14.04
FROM ubuntu:14.04

# Naming me as the maintainer
MAINTAINER Sebastien Bonami

# Installing WGET, GCC, LIBX11-DEV and MAKE
RUN sudo apt-get update && sudo apt-get install -y wget gcc libx11-dev make

# Installing EMBOSS 6.6.0
RUN wget ftp://emboss.open-bio.org/pub/EMBOSS/EMBOSS-6.6.0.tar.gz
RUN sudo tar -zxf /EMBOSS-6.6.0.tar.gz
RUN sudo rm /EMBOSS-6.6.0.tar.gz
RUN cd /EMBOSS-6.6.0 && sudo ./configure --prefix=/usr/local/emboss && sudo make && sudo make install
ENV PATH $PATH:/usr/local/emboss/bin

# Showing EMBOSS version at launch
RUN bash -c 'echo "embossversion" >> /.bashrc'