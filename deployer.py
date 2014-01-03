from __future__ import print_function

import os
import sys
from subprocess import check_output
from traceback import print_exc

from flask import abort, Flask, jsonify, request

app = Flask(__name__)


@app.route('/<secret>', methods=['POST'])
def post(secret):
  if secret != os.environ['SECRET']:
    abort(403)
  try:
    print('Deploying...')
    branch = request.json.get('ref').split('/')[2]
    cmds = [
      'rm -r output/'
      'pelican content',
      'rsync -r -m -h --delete --progress output/ /srv/pyconph/{branch}',
    ]
    print(check_output(' && '.join(cmds).format(branch=branch), shell=True))
  except:
    traceback.print_exc(file=sys.stderr)
    raise
  return jsonify(dict(ok=True))


if __name__ == '__main__':
  app.run(port=int(os.environ.get('PORT', 5000)))

