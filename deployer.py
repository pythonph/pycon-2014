from __future__ import print_function

import os
from subprocess import check_output

from flask import abort, Flask, json, jsonify, request


app = Flask(__name__)


def sh(cmd, **kwargs):
  print(check_output(cmd.format(**kwargs), shell=True))


@app.route('/<secret>', methods=['POST'])
def deploy(secret):
  if secret != os.environ['SECRET']:
    abort(403)
    
  payload = json.loads(request.form['payload'])
  branch = payload.get('ref').split('/')[2]
  
  sh(
    'git checkout -f {branch}',
    branch=branch,
  )
  sh(
    'pelican -d -o {root}/{branch} content',
    root=os.environ.get('ROOT', '/srv/pelican'),
    branch=branch,
  )

  return jsonify(dict(ok=True))


if __name__ == '__main__':
  app.run(port=int(os.environ.get('PORT', 5000)))
