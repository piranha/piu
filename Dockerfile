FROM alpine:3.7

RUN apk add --no-cache gcc musl-dev python2 python2-dev \
    py2-pip py2-pygments py2-bottle py2-tornado py2-jinja2

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

VOLUME ["/store"]
EXPOSE 80
COPY . /app/
RUN python setup.py --quiet install

CMD ["piud", "-a", "0.0.0.0", "-p", "80", "--path", "/store"]
