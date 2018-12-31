FROM python:3.6
RUN apt-get update \
    && apt-get upgrade -y --fix-missing \
    && apt-get install -y python3-pip

ADD . /usr/src/app
WORKDIR /usr/src/app
RUN chown -R 1000:1000 /usr/src/app
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt
VOLUME /usr/src/app
USER ${UID}