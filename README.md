PyCon Philippines
=================

Setup
-----
```sh
$ git clone https://github.com/pythonph/pycon.git && cd pycon
$ mkvirtualenv -a `pwd` pycon
$ pip install pelican
```

Develop
-------
```sh
$ ./develop_server.sh start
```

Push to deploy
--------------

Run deployer server

```sh
$ REMOTE=origin SECRET=<secret> ROOT=/srv/pycon PORT=<port> python ./deployer.py
```

Then add a service hook at Github: `http://<host>/<secret>`
