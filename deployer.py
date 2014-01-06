"""
Simple web server that listens for Github webhooks to implement push-to-deploy
with Pelican static sites

Settings are loaded from a json file except for SECRET which should be an 
environment variable

Example `deployer.json`

{
  "repos": {
    "mysite": {
      "root": "/path/to/repo",
      "remote": "origin",
      "output": "/srv/www/{branch}"
    }
  },
  "port": 5000
}

Run it

$ SECRET=thisisasecret python ./pelican_deployer.py deployer.json

Add http://<deployer_host>/mysite/thisisasecret as a webhook url and you're done
"""
import os
from subprocess import check_output

from flask import Flask, json, jsonify, request


app = Flask(__name__)


def sh(cmd, **kwargs):
  app.logger.info(check_output(cmd.format(**kwargs), shell=True))


@app.route('/<repo_id>/{}'.format(os.environ['SECRET']), methods=['POST'])
def deploy(repo_id):
  payload = json.loads(request.form['payload'])
  branch = payload.get('ref').split('/')[2]
  repo = app.config['repos'][repo_id]
  os.chdir(repo['root'])
  sh(
    'git pull {remote} {branch}',
    remote=repo.get('remote', 'origin'),
    branch=branch,
  )
  sh(
    'git checkout -f {branch}',
    branch=branch,
  )
  sh(
    'pelican -d -o {output} content',
    output=repo['output'].format(branch=branch, **payload),
  )
  return jsonify(dict(ok=True))


if __name__ == '__main__':
  with open('deployer.json') as f:
    app.config.update(**json.load(f))
  app.run(port=int(os.environ.get('PORT', 5000)))
