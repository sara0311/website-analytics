FROM python:3.5-slim

USER root

EXPOSE 8080

ARG workspace="none"

RUN apt-get update \
    && apt-get install --assume-yes wget

RUN wget https://codejudge-starter-repo-artifacts.s3.ap-south-1.amazonaws.com/backend-project/python/pre-build.sh
RUN chmod 775 ./pre-build.sh
RUN sh pre-build.sh

RUN wget https://codejudge-starter-repo-artifacts.s3.ap-south-1.amazonaws.com/backend-project/database/db-setup.sh
RUN chmod 775 ./db-setup.sh
RUN sh db-setup.sh

ENV JAVA_HOME /usr/lib/jvm/java-1.11.0-openjdk-amd64
RUN export JAVA_HOME

RUN wget https://codejudge-starter-repo-artifacts.s3.ap-south-1.amazonaws.com/backend-project/queue/queue-setup.sh
RUN chmod 775 ./queue-setup.sh
RUN sh queue-setup.sh

# Install Workspace for Python

RUN if [ $workspace = "theia" ] ; then \
	wget https://codejudge-starter-repo-artifacts.s3.ap-south-1.amazonaws.com/theia/pre-build.sh \
    && chmod 775 ./pre-build.sh && sh pre-build.sh ; fi

WORKDIR /var/


RUN if [ $workspace = "theia" ] ; then \
	wget https://codejudge-starter-repo-artifacts.s3.ap-south-1.amazonaws.com/theia/build.sh \
    && chmod 775 ./build.sh && sh build.sh ; fi

# Get RUN Script

WORKDIR /var/theia/

RUN if [ $workspace = "theia" ] ; then \
	wget https://codejudge-starter-repo-artifacts.s3.ap-south-1.amazonaws.com/theia/run.sh \
    && chmod 775 ./run.sh ; fi

# End Install for Workspace

RUN mkdir -p /var/app

WORKDIR /var/app

ADD requirements.txt /var/app

# Build the app
RUN wget https://codejudge-starter-repo-artifacts.s3.ap-south-1.amazonaws.com/backend-project/python/build.sh
RUN chmod 775 ./build.sh
RUN sh build.sh

ADD . .

# Run the app
RUN wget https://codejudge-starter-repo-artifacts.s3.ap-south-1.amazonaws.com/backend-project/python/django/run-3.sh
RUN chmod 775 ./run-3.sh
CMD sh run-3.sh