FROM registry.digitalocean.com/business-business/wordpress-base:latest
RUN apk update && apk add python3
RUN apk add --update coreutils && rm -rf /var/cache/apk/*
RUN pip3 install s3cmd
COPY run.sh /
COPY s3cfg /root
RUN mv /root/s3cfg /root/.s3cfg
RUN chmod +x /run.sh
ENTRYPOINT /run.sh
