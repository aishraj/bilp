FROM python:3.5

EXPOSE 8888

RUN apt-get update && apt-get install -y libpq-dev python-dev netcat-openbsd

# based on python:2.7-onbuild, but if we use that image directly
# the above apt-get line runs too late.
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
COPY dev.conf /usr/src/app/

RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD python botme.py