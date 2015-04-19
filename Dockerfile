FROM python:2

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN python setup.py install

CMD "piud -a 0.0.0.0 -p 5000 --path /store -d"
