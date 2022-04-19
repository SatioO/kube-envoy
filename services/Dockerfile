FROM python:3.8-slim-buster

WORKDIR /service

RUN apt-get update
RUN apt-get -q install curl --assume-yes

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000