from flask import Flask
from flask import request
from flask import jsonify

from github3 import GitHub
import jwt
from cryptography.hazmat.backends import default_backend
import time
import requests

from IssueProcessing import IssueProcessor
from Classifying import Classifier

app = Flask(__name__)

clf = Classifier()
base_url = 'https://api.github.com/repos/'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    action = data['action']
    if action == 'opened':
        owner, repo, number, title, body, labels = IssueProcessor().get_issue(data)
        if not labels:
            labels = clf.predict(title, body)
            bot = get_bot(owner, repo)
            issue_report = bot.issue(owner, repo, number)
            issue_report.add_labels(*labels)
    return ''

@app.route('/installation', methods=['GET', 'POST'])
def installation():
    return jsonify({'page':'https://github.com'})

def get_bot(owner, repo):
    app_id = '153786'
    installation_id = _get_installation_id(owner, repo, app_id)

    client = GitHub()
    fname = 'labelingbot.2022-01-13.private-key.pem'
    cert_str = open(fname, 'r').read().encode()

    client.login_as_app_installation(private_key_pem=cert_str, app_id=app_id, installation_id=installation_id)
    return client

def _app_headers(app_id):
    fname = 'labelingbot.2022-01-13.private-key.pem'
    cert_str = open(fname, 'r').read()
    cert_bytes = cert_str.encode()
    private_key = default_backend().load_pem_private_key(cert_bytes, None)

    now = int(time.time())
    payload = {
    'iat': now,
    'exp': now + (10 * 60),
    'iss': app_id
    }

    actual_jwt = jwt.encode(payload, private_key, algorithm='RS256')

    headers = {"Authorization": "Bearer {}".format(actual_jwt),
            "Accept": "application/vnd.github.v3+json"}
    return headers

def _get_installation_id(owner, repo, app_id):
    url = base_url+'{}/{}/installation'.format(owner, repo)
        
    response = requests.get(url=url, headers=_app_headers(app_id))
    if response.status_code != 200:
        raise Exception('Status code : {}, {}'.format(response.status_code, response.json()))
    return response.json()['id']

if __name__ == '__main__':
    app.run('0.0.0.0', '5000')


###  Expansion work in progress  ###

# @app.route('/installation', methods=['GET', 'POST'])
# def installation():
#     return redirect(url_for("labelsSelection"))

# @app.route('/LabelsSelection', methods=['GET'])
# def labelsSelection():
#     return render_template("LabelsSelectForm.html")

# @app.route('/RepositoriesInformation', methods=['GET', 'POST'])
# def getRepositoriesInfo():
#     global repo_label
#     if request.method == 'GET':
#         return jsonify(repo_label)
#     elif request.method=='POST':
#         ## {repository: [label, label, ...], repository: [label, label, ...], ...}
#         selectedLabels = json.loads(request.get_data())
#         return jsonify({'page':'crawlCycleSetting'})

# @app.route('/crawlCycleSetting')
# def crawlCycleSetting():
#     return render_template('crawlCycleSettingForm.html')

# @app.route('/crawlCycleSetting/submit', methods=["POST"])
# def submitForm():
#     selectedDayTime = json.loads(request.get_data())
#     return jsonify({'page':'https://github.com'})