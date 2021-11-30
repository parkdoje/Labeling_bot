from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import jsonify
from dataExtractor import DataExtrator
from issueProcessor import IssueProcessor
import json
import requests

app = Flask(__name__)
access_token = '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'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    action = data['action']
    if action == 'opened':
        IssueProcessor().attach_label(data, access_token)
    return ''

@app.route('/installation', methods=['GET', 'POST'])
def installation():
    global repo_label
    global access_token
    repo_label = {}
    dataExtractor = DataExtrator()
    if request.method == 'GET':
        ## properties = code, installation_id, setup_action
        properties = request.full_path.split('?')[-1].split('&')
        code = properties[0].split('=')[-1]
        installation_id = properties[1].split('=')[-1]

        access_token = dataExtractor.getAccessToken(code)
        ## repos are selected while install phase of github. ** full_name: ex) john3205/I2M = $owner/$repository_name
        repositories = dataExtractor.getRepositories(access_token, installation_id)

        ## repository = full_name
        data = []
        for repository in repositories:
            labels = dataExtractor.getLabelsForProject(access_token, repository)
            data.append([repository, access_token, labels])
            repo_label[repository] = labels

        ## data = [[repository, access_token, labels], [repository, access_token, labels], ...]

    return redirect(url_for("labelsSelection"))

@app.route('/LabelsSelection', methods=['GET'])
def labelsSelection():
    return render_template("LabelsSelectForm.html")

@app.route('/RepositoriesInformation', methods=['GET', 'POST'])
def getRepositoriesInfo():
    global repo_label
    if request.method == 'GET':
        return jsonify(repo_label)
    elif request.method=='POST':
        ## {repository: [label, label, ...], repository: [label, label, ...], ...}
        selectedLabels = json.loads(request.get_data())
        return jsonify({'page':'crawlCycleSetting'})

@app.route('/crawlCycleSetting')
def crawlCycleSetting():
    return render_template('crawlCycleSettingForm.html')

@app.route('/crawlCycleSetting/submit', methods=["POST"])
def submitForm():
    selectedDayTime = json.loads(request.get_data())
    print(selectedDayTime)
    return jsonify({'page':'https://github.com'})

if __name__ == '__main__':
    app.run('0.0.0.0', '5000')
