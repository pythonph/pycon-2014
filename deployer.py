import os
from subprocess import check_output

from flask import Flask, json, jsonify, request

app = Flask(__name__)


def sh(cmd, **kwargs):
  app.logger.info(check_output(cmd.format(**kwargs), shell=True))


@app.route('/{}'.format(os.environ['SECRET']), methods=['POST'])
def deploy():
  payload = json.loads(request.form['payload'])
  branch = payload.get('ref').split('/')[2]

  sh(
    'git pull {remote} {branch}',
    remote=os.environ.get('REMOTE', 'origin'),
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

