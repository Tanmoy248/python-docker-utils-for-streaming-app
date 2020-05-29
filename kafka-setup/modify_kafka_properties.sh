#!/bin/bash

#docker ps -a

#echo "hostname : $1"
kafkaIp=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kafka-docker_kafka_1`

#add kafka-python network gateway ip 
kafkaNetworkIp=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}' $2`

#add kafka-python hostname on assignment dockerkf
docker exec -d assignment_codes bash -c "echo '$kafkaNetworkIp $1' >> /etc/hosts"

echo "$kafkaNetworkIp | $kafkaIp"

 
