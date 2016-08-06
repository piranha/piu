FROM alpine

RUN apk add --no-cache curl tar xz ca-certificates gcc python python-dev && update-ca-certificates

RUN mkdir /app
WORKDIR /app
COPY . /app/
VOLUME ["/store"]
EXPOSE 80

RUN python setup.py install

CMD ["piud", "-a", "0.0.0.0", "-p", "80", "--path", "/store"]
