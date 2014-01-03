from __future__ import print_function

import os
import traceback
from subprocess import check_output

from flask import abort, Flask, json, jsonify, request

app = Flask(__name__)


@app.route('/<secret>', methods=['POST'])
def post(secret):
  if secret != os.environ['SECRET']:
    abort(403)
  try:
    print('Deploying...')
    payload = json.loads(request.form['payload'])
    branch = payload.get('ref').split('/')[2]
    cmds = [
      'rm -rf output/',
      'pelican content',
      'rsync -r -m -h --delete --progress output/ {root}/{branch}',
    ]
    print(check_output(' && '.join(cmds).format(
      root=os.environ.get('ROOT', '/srv/pelican'),
      branch=branch,
    ), shell=True))
  except Exception:
    traceback.print_exc()
    raise
  return jsonify(dict(ok=True))


if __name__ == '__main__':
  app.run(port=int(os.environ.get('PORT', 5000)))
