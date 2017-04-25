#!/bin/sh
wget http://www.apache.org/dist/mesos/1.2.0/mesos-1.2.0.tar.gz

tar -zxf mesos-1.2.0.tar.gz

# Update the packages.
sudo apt-get update

# Install a few utility tools.
sudo apt-get install -y tar wget git

# Install the latest OpenJDK.
sudo apt-get install -y openjdk-8-jdk

# Install other Mesos dependencies.
sudo apt-get -y install build-essential python-dev python-virtualenv libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev zlib1g-dev

# Change working directory.
cd mesos-1.2.0

# Configure and build.
mkdir build
cd build
../configure
make

# Run test suite.
make check
