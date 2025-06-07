FROM python:3.8-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
WORKDIR /Ultra-Forward-Bot
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN JishuDeveloper /Ultra-Forward-Bot

COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]
