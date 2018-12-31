FROM python:3.6
RUN apt-get update \
    && apt-get upgrade -y --fix-missing \
    && apt-get install -y build-essential python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev

ADD . /usr/src/app
WORKDIR /usr/src/app
RUN chown -R 1000:1000 /usr/src/app
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
ENV FLASK_APP=server.py
VOLUME /usr/src/app
USER ${UID}

RUN flask run --host=0.0.0.0