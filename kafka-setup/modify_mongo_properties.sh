#!/bin/bash

#docker ps -a
#echo "hostname : $1"
mongoIp=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $2`

#add mongo-dev hostname on assignment docker
docker exec -d assignment_codes bash -c "echo '$mongoIp $1' >> /etc/hosts"
echo $mongoIp

 
