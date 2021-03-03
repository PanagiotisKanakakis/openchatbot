import json
import os
from json import JSONEncoder

import fasttext
import nltk
import numpy
import numpy as np
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer

STOP_WORDS = nltk.corpus.stopwords.words('english')
STOP_WORDS.append('Selfie')
STOP_WORDS.append('SELFIE')
STOP_WORDS.append('selfie')


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class FastTextClassifier:

    def __init__(self, languageCode):
        self.languageCode = languageCode
        if os.path.exists(os.path.join(os.getcwd(), 'files/models/' + self.languageCode + '.bin')):
            self.model = fasttext.load_model(os.path.join(os.getcwd(), 'files/models/' + self.languageCode + '.bin'))

    def clean_up_sentence(self, sentence):
        stemmer = LancasterStemmer()
        # tokenize the pattern
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    def bow(self, sentence, show_details=False):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words
        bag = [0] * len(self.data['words'])
        for s in sentence_words:
            for i, w in enumerate(self.data['words']):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)

        return np.array(bag)

    def classify(self, sentence):
        sentence = self.preprocess(sentence)
        prediction = self.predict(sentence)
        utterance = self.utter(prediction)
        return utterance

    def predict(self, query):
        texts = [query]
        prediction = json.dumps(self.model.predict(texts, k=-1), cls=NumpyArrayEncoder)
        return prediction

    def utter(self, prediction):
        response_file = open(os.path.join(os.getcwd(), 'files/response_data/' + self.languageCode + '.json'), 'r')
        responses = json.loads(response_file.read())
        labels = json.loads(prediction)[0][0]
        confidences = json.loads(prediction)[1][0]
        return [(responses[labels[0]], confidences[0])]

    def preprocess(self, sentence):
        filtered_sentence = ''
        line_token = word_tokenize(sentence)
        remove_sw = [word for word in line_token if not word in STOP_WORDS]
        filtered_sentence += ' '.join(remove_sw)
        return filtered_sentence
