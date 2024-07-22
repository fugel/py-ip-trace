# syntax=docker/dockerfile:1

FROM python:3.13.0b4-alpine3.20

WORKDIR /python-docker

# RUN apt update
# RUN apt install mtr -y
RUN apk update
RUN apk add mtr

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]