#!/bin/bash

#docker ps -a
#echo "hostname : $1"
sparkIp=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $2`

#add spark-dev hostname on assignment docker
docker exec -d assignment_codes bash -c "echo '$sparkIp $1' >> /etc/hosts"

echo $sparkIp

 
