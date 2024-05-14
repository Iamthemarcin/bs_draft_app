FROM ubuntu:22.04

WORKDIR /usr/src/app

#no bufferin before terminal
ENV PYTHONBUFFERED = 1


RUN apt update && apt upgrade
RUN apt install python3 python3-pip -y

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apt install libpq-dev python3-dev libcairo2-dev pkg-config python3-apt -y 

RUN pip3 install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]