FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .
#COPY gunicorn_starter.sh .

RUN apk update
RUN apk add build-base
RUN pip install -r requirements.txt

#RUN ["chmod", "+x", "gunicorn_starter.sh"]

#RUN ["/bin/sh"]
#ENTRYPOINT ["./gunicorn_starter.sh"]
CMD [ "gunicorn", "api:app", "-w", "2", "--threads", "2", "-b" ,"0.0.0.0:8000", "--reload"]