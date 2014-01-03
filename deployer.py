import os
from subprocess import call

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def post():
  branch = request.json.get('ref').split('/')[2]
  cmds = [
    'rm -r output/'
    'pelican content',
    'rsync -r -m -h --delete --progress output/ /srv/pyconph/{branch}',
  ]
  call(' && '.join(cmds).format(branch=branch), shell=True)


if __name__ == '__main__':
  app.run(port=os.environ.get('PORT', 5000))

