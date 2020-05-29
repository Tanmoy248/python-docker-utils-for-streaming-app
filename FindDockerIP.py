#####################################
# Description: The idea of this
# is to find the IP of each running
# docker using docker inspect

# Example : docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' c1fadfa46d82
######################################

import subprocess
import os
import sys
from time import sleep

def createContainerMap():
    dockerNameMap= {
        'kafka': {"repo": "kafka-docker_kafka" , "imgName": "kafka-docker_kafka_1", "hostname" : "kafka-python", "port":9093, "IP":None},
        'spark':{"repo": "bitnami/spark" , "imgName": "spark-dev", "hostname" : "spark-dev", "port":7077, "IP":None},
        'mongo':{"repo": "mongo" , "imgName": "mongo", "hostname" : "mongo-dev", "port":27017, "IP":None},
        'assignment_codes':{"repo": "my-submission" , "imgName": "assignment_codes", "hostname" : "assignment_codes", "port":8080, "IP":None}
    }
    expectedDir=os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()
    if (cwd != expectedDir):
        sys.exit("Please execute the command from {} directory only".format(__file__))
    else:
        beignDownloads(expectedDir)
        runSparkMongo(dockerNameMap)
        ipStatus(expectedDir,dockerNameMap)
        sparkSubmitCmd = assignmentSetup(dockerNameMap)
        print("\n")
        print("please execute this in the assignment_codes docker ---->")
        print(sparkSubmitCmd)
    #print(dockerNameMap)


def beignDownloads(expectedDir):
    #cmd1 = "sudo ls -l ~/Downloads"
    cmd2 = "docker pull bitnami/spark"
    cmd3 = "docker pull mongo"

    dockers = [cmd2, cmd3]

    print("Begin downloads. Current location should be ", expectedDir)

    for cmd in dockers:
        print("Download image for {}....".format(cmd.split(" ")[2]))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        print(stdout, stderr)

    # now execute docker run command as per the map below:
    cmd1 = "docker-compose up -d"
    print("Kafka setup will begin...")

    kafkaSetupDir = expectedDir + '/kafka-setup/kafka-docker/'
    print("Executing kafka startup commands from :",kafkaSetupDir,"....")
    os.chdir(kafkaSetupDir.strip())
    print("change directory " + os.getcwd())
    p = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    print(stdout, stderr)

def ipStatus(expectedDir,dockerNameMap):
    kafkaSetup=expectedDir + '/kafka-setup/'

    for key in dockerNameMap:
        record = dockerNameMap.get(key)
        hostname = record.get('hostname')
        imgName = record.get('imgName')
        cmdIp = "bash -x modify_{}_properties.sh {} {}".format(key,hostname,imgName)
        os.chdir(kafkaSetup)
        print("Current dir:",kafkaSetup)

        p = subprocess.Popen(cmdIp, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        print("Status of {}".format(key), stdout, stderr, type(stdout))
        stdoutCleanup = stdout.decode("utf-8").split("|")
        cleanIp = ""
        if (len(stdoutCleanup) > 1):
            cleanIp = "{} | Docker Ip:{}".format(stdoutCleanup[0], stdoutCleanup[1])
        else:
            cleanIp = stdout.decode("utf-8")
        print("stdoutCleanup ", stdoutCleanup)
        print("{} is running...".format(key))
        dockerNameMap.get(key)['IP']=cleanIp
        sleep(3)

def runSparkMongo(dockerNameMap):
    for key in dockerNameMap:
        if key == 'kafka':
            pass
        else:
            repo = dockerNameMap.get(key).get('repo')
            imgname = dockerNameMap.get(key).get('imgName')
            host = dockerNameMap.get(key).get('hostname')
            dockerRunCmd = "docker run --name {name} -d -i -t -h {host} {repo}:latest".format(
                name=imgname,host=host,repo=repo
            )
            print("Executing...", dockerRunCmd)
            p = subprocess.Popen(dockerRunCmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
            print("Status of ",key , stdout, stderr, type(stdout))
            print(key)

def assignmentSetup(dockerNameMap):
    # for kafka, it is on a different subnet
    # so we need to fetch the network gateway address
    # the command generated at the end shoud be executed so submit the job to spark cluster
    yourEtcHosts = ""
    sparkSubmitCmd = 'export SPARK_LOCAL_HOSTNAME=localhost;export KAFKA_BROKERS="{brokers}";spark-submit --class "Main" --master spark://{sparkHost}:7077 /app/spark/coursera-assembly-0.1.jar'
    brokers=""
    sparkHost=""
    for key in dockerNameMap:
        record = dockerNameMap.get(key)
        hostname = record.get('hostname')
        ip = ""
        port = record.get('port')
        tmpIp = str(record.get('IP')).split("|")
        print("----", tmpIp)
        if len(tmpIp) > 1:
            ip = tmpIp[0].strip('\n').strip()
        else:
            ip = tmpIp[0].strip('\n').strip()
        yourEtcHosts = yourEtcHosts + ip + '\t' + hostname + '\n'

        # get spark host and kafka broker

        if key == 'spark':
            sparkHost = hostname
        elif key == 'kafka':
            brokers = hostname + ":" + str(port)
        else:
            pass

    print("\n\n")
    print("/etc/hosts entries : ")
    print(yourEtcHosts)
    result = sparkSubmitCmd.format(brokers=brokers, sparkHost=sparkHost)
    return result

if __name__ == '__main__':
    createContainerMap()




