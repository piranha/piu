# paste.in.ua

That's a simple pastebin service, written in Python (look in `setup.py` for
dependencies). Read [about](http://paste.in.ua/about/) page if you want to know
more.

## How to run

I run it in [Dokku](https://github.com/progrium/dokku), so just read
`Dockerfile` for the instructions.

`piud` opens an HTTP port and it requires writeable directory to store data
in. That's all.
