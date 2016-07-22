FROM python@sha256:ad39551743b356efda7c61f46019b97d49d1aab01b97f0e6d87c9b34326f3bfe
#Python 2.7
MAINTAINER Justin Littman <justinlittman@gwu.edu>

RUN apt-get update && apt-get install -y git
RUN pip install pip==7.1.2
RUN pip install git+git://github.com/gwu-libraries/pywb.git@master
#Install appdeps to allow checking for application dependencies
RUN pip install appdeps
COPY *.yaml /opt/sfm-wayback/
WORKDIR /opt/sfm-wayback

EXPOSE 8080
#This links in sfm-utils as develop.
CMD appdeps.py --wait-secs 90 --file-wait /sfm-data/wayback/collections/sfm \
    && cp *.yaml /sfm-data/wayback \
    && cd /sfm-data/wayback \
    && wayback -d /sfm-data/wayback
