import json
import os

import fasttext
from chatterbot.trainers import Trainer


def createFile(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)


class ChatterBotFastTextTrainer(Trainer):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.httpClient = None

    def setHttpClient(self, httpClient):
        self.httpClient = httpClient

    def train(self):
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
                train_data += train_data
                train_data += train_data
                train_file.write(train_data)
                response_file.write(json.dumps(response_data))
                train_file.close()
                response_file.close()
                model = fasttext.train_supervised(input=train_file_name, lr=0.5, epoch=25, wordNgrams=2)
                model_file_name = os.path.join(os.getcwd(), 'files/models/' + languageCode + '.bin')
                createFile(model_file_name)
                model.save_model(model_file_name)
