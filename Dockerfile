FROM python:3.11-alpine

MAINTAINER sadminriley

ADD requirements.txt /

RUN pip install -r /requirements.txt

COPY lib/* /


CMD [ "python", "./flask_upload.py" ]
