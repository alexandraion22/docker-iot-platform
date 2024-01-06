FROM python:latest

COPY requirements.txt /tmp
RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt
RUN apt-get update && apt-get install -y netcat-traditional

ADD adapter.py start_adapter.sh /adapter/
WORKDIR /adapter

ADD start_adapter.sh /
RUN chmod +x /start_adapter.sh

CMD ["./start_adapter.sh"]
