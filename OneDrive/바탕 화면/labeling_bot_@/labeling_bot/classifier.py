import fasttext
import numpy as np

class Classifier:
    def __init__(self):
        self.model_path = './labeling_model.bin'

    def train(self):
        model = fasttext.load_model(self.model_path)
        self._save(model)

    def predict(self, title, body):
        model = fasttext.load_model(self.model_path)
        text = '{} {}'.format(title, body.replace('\n', ' '))
        labels_acc = model.predict(text, k=2, threshold=0.1) ## form = ((l, l, l), (a, a, a))
        labels = [label.replace('__label__', '') for label in labels_acc[0]]
        return labels

    def _save(self, model):
        model.save_model(self.model_path)

        
