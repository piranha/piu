FROM python:2-alpine

RUN apk add --no-cache ca-certificates gcc && update-ca-certificates

RUN mkdir /app
WORKDIR /app
COPY . /app/
VOLUME ["/store"]
EXPOSE 80

RUN python setup.py install

CMD ["piud", "-a", "0.0.0.0", "-p", "80", "--path", "/store"]
