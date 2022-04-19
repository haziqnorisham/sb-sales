FROM python:3.10-buster

RUN mkdir /flask_app

COPY requirements.txt /flask_app/requirements.txt

WORKDIR /flask_app

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD python3 server.py
