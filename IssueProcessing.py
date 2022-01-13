class IssueProcessor:
    def __init__(self):
        pass

    @classmethod
    def get_issue(cls, data):
        issue = data['issue']
        repository = issue['repository_url'] ## full_name

        owner, repo = repository.split('/')[-2:]
        number = issue['number']
        title = issue['title']
        body = issue['body']
        labels = [label['name'] for label in issue['labels']]

        return owner, repo, number, title, body, labels