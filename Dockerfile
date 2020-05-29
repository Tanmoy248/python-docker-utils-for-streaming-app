FROM ubuntu 
MAINTAINER demousr@gmail.com 

# Install dependencies
RUN apt-get update && \
        apt-get -qq -y install curl && \
        apt-get -y install vim && \
        apt-get -y install wget && \
#        apt-get -y install python3 && \
#        apt-get -y install python3-pip && \
#        apt-get -y install net-tools && \
        apt-get -y install openjdk-8-jdk && \ 
#        apt-get -y install docker.io && \
            rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/spark/

ADD docker-entrypoint.sh /usr/local/bin/
VOLUME ["/app/"]

# Define working directory
WORKDIR /app/

#setup JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
RUN export JAVA_HOME
ENV PATH $JAVA_HOME/bin:$PATH:/app/:/usr/bin/bash/

ADD coursera-assembly-0.1.jar /app/spark
RUN chmod +x /app/spark/coursera-assembly-0.1.jar
#RUN curl "https://drive.google.com/open?id=1lSD9JKMbacQeCDp3-m-doZsF7DOQC0Ao" -o /app/spark/spark-streams.jar --tlsv1

#add spark tar file to container
ADD "spark-3.0.0-preview2-bin-hadoop2.7.tgz" /usr/lib
RUN chmod +x /app/spark/*
RUN echo $(ls -l /app/spark)

#RUN cd /app/spark && tar -C /app/spark -xzvf "/app/spark/spark-3.0.0-preview2-bin-hadoop2.7.tgz" && \

RUN  mv /usr/lib/spark-3.0.0-preview2-bin-hadoop2.7 /usr/lib/spark 
    
RUN echo $(pwd)
RUN echo $(ls -l /app/spark)
#RUN mv /app/spark/spark-3.0.0-preview2-bin-hadoop2.7 /app/spark/spark
RUN  echo $(ls -l /usr/lib)
ENV SPARK_HOME /usr/lib/spark
ENV PATH $PATH:$SPARK_HOME/bin 



#give permission to entry_point script
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
 
#CMD [“echo”,”Image created”
ENTRYPOINT ["docker-entrypoint.sh"]
CMD tail -f /dev/null
