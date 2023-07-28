FROM ubuntu
MAINTAINER Parth
RUN apt-update
CMD ["echo","this is my first ubuntu image"]


WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt


