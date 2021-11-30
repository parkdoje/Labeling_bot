import fasttext
import re
from nltk.corpus import stopwords


class Classifier:

    def classify(title, body):
        text = title + ' ' + body.replace('\n', ' ')
        
        model = fasttext.load_model('./labeling_model.bin')

        ##레이블 추출
        labels = model.predict(text, k=2 ,threshold=0.1)
        ## labels : __label__bug, __label__enhancement

        label_list = list((labels))
        label_list = list((label_list[0]))

        for i in range(len(label_list)):
            label_list[i] = label_list[i].replace('__label__', '')
        
        
        return label_list
