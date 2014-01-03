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

Deployer
--------

Run deployer server

```sh
$ PORT=<port> SECRET=<secret> python ./deployer.py
```

Then add a service hook at Github: `http://<host>/<secret>`
