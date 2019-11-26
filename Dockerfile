FROM alpine:3.9

RUN apk add --update --no-cache --virtual=run-deps \
  python3 \
  ca-certificates \
  && rm -rf /var/cache/apk/*

RUN mkdir -p /opt/echo-fs
WORKDIR /opt/echo-fs

COPY requirements.txt /opt/echo-fs/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY run_and_set_ec2_ip.sh /opt/echo-fs
RUN chmod +x /opt/app/run_and_set_ec2_ip.sh

COPY app /opt/echo-fs
