FROM python@sha256:ad39551743b356efda7c61f46019b97d49d1aab01b97f0e6d87c9b34326f3bfe
#Python 2.7
MAINTAINER Justin Littman <justinlittman@gwu.edu>

RUN apt-get update && apt-get install -y \
    git=1:2.1.4-2.1+deb8u1
RUN pip install pip==7.1.2
#This pre-fetches the most recent requirements.txt.
ADD https://raw.githubusercontent.com/gwu-libraries/sfm-wayback/master/requirements/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN pip install appdeps
WORKDIR /opt/sfm-wayback
#This links in sfm-utils as develop.
CMD pip install -r requirements/requirements.txt --upgrade \
    && appdeps.py --port-wait mq:5672 \
    && python sfm_wayback_loader.py mq $MQ_ENV_RABBITMQ_DEFAULT_USER $MQ_ENV_RABBITMQ_DEFAULT_PASS wayback_indexer_$HOSTNAME /sfm-data/wayback --debug=$DEBUG
