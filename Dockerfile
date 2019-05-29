FROM python:3.7-alpine AS prod

MAINTAINER apollovy "apollovy@gmail.com"

WORKDIR /app

RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        build-base \
        mariadb-dev

COPY run.py run.py
COPY requirements.txt requirements.txt
COPY requirements requirements
RUN pip install -r requirements.txt

RUN apk del .build-deps


COPY ready_for_sky ./

ENV PYTHONPATH ready_for_sky

CMD python run.py

FROM prod AS test

RUN pip install -r requirements/test.txt
CMD pytest ready_for_sky tests
