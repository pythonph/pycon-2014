from __future__ import print_function

import os
from subprocess import check_output

from flask import abort, Flask, jsonify, request

app = Flask(__name__)


@app.route('/<secret>')
def post(secret):
  if secret != os.environ['SECRET']:
    abort(403)
  branch = request.json.get('ref').split('/')[2]
  cmds = [
    'rm -r output/'
    'pelican content',
    'rsync -r -m -h --delete --progress output/ /srv/pyconph/{branch}',
  ]
  print(check_output(' && '.join(cmds).format(branch=branch), shell=True))
  return jsonify(dict(ok=True))


if __name__ == '__main__':
  app.run(port=int(os.environ.get('PORT', 5000)))

