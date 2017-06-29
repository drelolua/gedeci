FROM alpine:latest

RUN apk -U add  bash \
                gcc \
                g++ \
                python \
                python2-dev \
                openssl \
                openssl-dev \
                curl curl-dev \
                py2-pip
RUN pip install tornado pymongo pycurl simplejson redis
RUN mkdir /root/gedeci-com

EXPOSE 8001

ENTRYPOINT ["/root/gedeci-com/gedeciserver.py"]


