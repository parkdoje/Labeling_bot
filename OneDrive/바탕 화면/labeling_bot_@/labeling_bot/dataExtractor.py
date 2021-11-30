import json
import requests

class DataExtrator:
    def __init__(self):
        self.client_id = 'Iv1.ae4d7501e4c055cc'
        self.client_secret = '04b3390029f2f436e0a76bd8cb2b1c10d6f1d448'
    
    def getAccessToken(self, code):
        url = 'https://github.com/login/oauth/access_token'
        headers = {'Content-Type': 'application/json'}
        data = {'client_id': self.client_id, 'client_secret': self.client_secret, 'code': code}

        response = requests.post(url, headers=headers, data=json.dumps(data))

        contents = str(response.content).split('&')
        access_token = contents[0].split('=')[-1]
        return access_token

    def getRepositories(self, access_token, installation_id):
        url = 'https://api.github.com/user/installations/{}/repositories'.format(installation_id)
        headers = {'Authorization': 'token {}'.format(access_token), 'Accept': 'application/vnd.github.v3+json'}

        response = requests.get(url, headers=headers)
        repositories = response.json()['repositories']
        repositories = [repo['full_name'] for repo in repositories]
        return repositories

    def getLabelsForProject(self, access_token, repository):
        url = 'https://api.github.com/repos/{}/labels'.format(repository)
        headers = {'Authorization': 'token {}'.format(access_token), 'Accept': 'application/vnd.github.v3+json'}

        response = requests.get(url, headers=headers)
        labels = [label['name'] for label in json.loads(response.content.decode('utf-8'))]
        return labels
