FROM python:3.9-slim-buster

WORKDIR /articles

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /articles/app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]