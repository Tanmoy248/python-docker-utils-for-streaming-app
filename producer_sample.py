# generate some sample records to the kafka container
from kafka import KafkaProducer
from time import sleep
import sys

def produceToKafka(topic, filename,brokers) :
    producer = KafkaProducer(bootstrap_servers=[brokers]
                             )
    with open(filename, 'rb') as f1:
        for message in f1:
            print("sending msg :",message)
            if type(topic) == bytes:
                topic = topic.decode('utf-8')
            producer.send(topic, message)
            sleep(5)

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Please pass kafka brokers as mentioned in output of FindDockerIp.py")
        print(sys.argv)
    else:
        brokers=sys.argv[1]
        print("Producing to ", brokers)
        produceToKafka("lalamove-test-1", "data_2.json",brokers)