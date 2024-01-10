FROM python:latest

RUN pip3 install --upgrade pip

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

RUN apt-get update
RUN apt-get install -y netcat-traditional

ADD adapter.py start_adapter.sh /adapter/
WORKDIR /adapter

ADD start_adapter.sh /
RUN chmod +x /start_adapter.sh
CMD ["./start_adapter.sh"]
