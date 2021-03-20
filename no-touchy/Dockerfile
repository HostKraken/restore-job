FROM registry.digitalocean.com/business-business/wordpress-base:latest
RUN apk update && apk add python3
RUN apk add --update coreutils && rm -rf /var/cache/apk/*
RUN pip3 install s3cmd kubernetes
COPY run.sh /
COPY s3cfg /root
COPY delete.py /
RUN mv /root/s3cfg /root/.s3cfg
RUN chmod +x /run.sh
RUN chmod +x /delete.py
ENTRYPOINT /run.sh
