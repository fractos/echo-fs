FROM ubuntu
RUN apt-get update -y && apt-get install -y python-pip
COPY app /opt/echo-fs
WORKDIR /opt/echo-fs
RUN pip install -r requirements.txt
