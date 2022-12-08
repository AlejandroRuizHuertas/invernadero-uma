FROM python:3.10-slim


COPY requirements.txt /
COPY worker_starter.sh /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

RUN chmod +x worker_starter.sh
CMD ["/bin/sh", "worker_starter.sh"]
