#Dockerfile
FROM python:3.6

RUN mkdir /app

WORKDIR "/app"

ADD ./ /app

ENTRYPOINT [ "python", "samuellehman_pa4.py" ]