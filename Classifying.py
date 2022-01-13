import fasttext

class Classifier:
    def __init__(self):
        self.model_path = './vscode_model.bin'
        self.model = fasttext.load_model(self.model_path)

    def train(self):
        ## training ##
        self._save()

    def _save(self):
        self.model.save(self.model_path)

    def predict(self, title, body):
        text = '{} {}'.format(title, body.replace('\n', ' '))
        ## text_preprocessing ##
        labels_acc = self.model.predict(text, k=-1, threshold=0.1) ## form = ((l, l, l), (a, a, a))
        labels = [label.replace('__label__', '') for label in labels_acc[0]]
        return labels