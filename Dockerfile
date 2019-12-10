FROM python:3.8-alpine

LABEL maintainer="Leon Jacobs <leonja511@gmail.com>"

WORKDIR /app
ADD . /app
RUN python setup.py install

ENTRYPOINT ["loadsheddingstatus"]