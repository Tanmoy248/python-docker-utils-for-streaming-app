#!/bin/bash

#docker ps -a
#echo "hostname : $1"
assignIp=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $2`

echo $assignIp

 
