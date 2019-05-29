FROM python:3.7-alpine

MAINTAINER apollovy "apollovy@gmail.com"

WORKDIR /app
ADD . /app/

RUN pip install -r requirements.txt

ENV PYTHONPATH ready_for_sky

CMD python run.py
