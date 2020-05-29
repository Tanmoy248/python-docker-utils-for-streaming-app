#!/bin/bash

#=============================================
# Description: Verify all the dependent 
#              software is installed 
#=============================================

set -e

apt-get update

which python3
if [ $? -ne 0 ]
then
apt-get install python3
apt-get install python3-pip
fi

which docker
if [ $? -ne 0 ]
then
apt-get install docker
fi

# set any additional dependencies

