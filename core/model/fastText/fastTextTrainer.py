import os

import fasttext
import json
import nltk
from chatterbot.trainers import Trainer
from nltk import word_tokenize

STOP_WORDS = nltk.corpus.stopwords.words('english')
STOP_WORDS.append('Selfie')
STOP_WORDS.append('SELFIE')
STOP_WORDS.append('selfie')


def createFile(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)


class ChatterBotFastTextTrainer(Trainer):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.httpClient = None

    def setHttpClient(self, httpClient):
        self.httpClient = httpClient

    def transformDataset(self, train_data):
        dataToConvert = train_data
        train_data += train_data.lower()
        train_data += train_data.lower()
        train_data += train_data.lower()
        train_data += train_data.lower()
        train_data += train_data.lower()
        train_data += train_data.lower()
        dataToConvert = dataToConvert.replace('SELFIE', '')
        dataToConvert = dataToConvert.replace('selfie', '')
        dataToConvert = dataToConvert.replace('Selfie', '')
        train_data += dataToConvert.lower()
        train_data += dataToConvert.lower()
        train_data += dataToConvert.lower()
        train_data += dataToConvert.lower()
        train_data += dataToConvert.lower()
        train_data += dataToConvert.lower()
        return train_data

    def preprocess(self, line):
        filtered_line = ''
        line_token = word_tokenize(line)
        remove_sw = [word for word in line_token if not word in STOP_WORDS]
        filtered_line += ' '.join(remove_sw)
        filtered_line += '\n'
        return filtered_line.replace(' ', '\t', 1)

    def train(self):
        languageCode = 'en'
        train_file_name = os.path.join(os.getcwd(), 'files/train_data/' + languageCode + '.txt')

        data = ''
        with open(train_file_name) as fp:
            line = fp.readline()
            while line:
                data += self.preprocess(line)
                line = fp.readline()

        # train_file_name = os.path.join(os.getcwd(), 'files/train_data/' + languageCode + 'filtered.txt')
        # train_file = open(train_file_name, 'w+')
        # train_file.write(data)
        # train_file.close()
        languages = self.httpClient.getAllLanguages()
        for language in languages:
            languageCode = language['code']
            if languageCode == 'en':
                train_data = ''
                response_data = {}
                train_file_name = os.path.join(os.getcwd(), 'files/train_data/' + languageCode + '.txt')
                response_file_name = os.path.join(os.getcwd(), 'files/response_data/' + languageCode + '.json')

                createFile(train_file_name)
                createFile(response_file_name)

                train_file = open(train_file_name, 'w+')
                response_file = open(response_file_name, 'w+')
                questions = self.httpClient.getQuestionsPerLanguage(languageCode)
                for question in questions:
                    answer = question['answer']
                    train_data += '__label__' + str(answer['id']) + ' ' + question[
                        'description'] + '\n'

                    response_data['__label__' + str(answer['id'])] = answer['description']

                # train_data = self.transformDataset(train_data)
                train_file.write(train_data)
                response_file.write(json.dumps(response_data))
                train_file.close()
                response_file.close()
        hyper_params = {"lr": 1.0,
                        "epoch": 50,
                        "wordNgrams": 2,
                        "minn": 3,
                        "maxn": 5,
                        "dim": 100}
        model = fasttext.train_supervised(input=train_file_name, **hyper_params)
        model_file_name = os.path.join(os.getcwd(), 'files/models/' + languageCode + '.bin')
        createFile(model_file_name)
        model.save_model(model_file_name)
