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
        print(languages)
        topics = self.httpClient.getAllTopics()
        print(topics)
        for language in languages:
            languageCode = language['code']
            train_data = ''
            response_data = {}
            train_file_name = os.path.join(os.getcwd(), 'files/train_data/' + languageCode + '.txt')
            response_file_name = os.path.join(os.getcwd(), 'files/response_data/' + languageCode + '.json')

            createFile(train_file_name)
            createFile(response_file_name)

            train_file = open(train_file_name, 'w+')
            response_file = open(response_file_name, 'w+')
            for topic in topics:
                topicId = topic["id"]
                questions = self.httpClient.getQuestionPerTopicAndLanguage(topicId, languageCode)
                for question in questions:
                    train_data += '__label__' + str(topicId) + ' ' + question['description'] + '\n'
                    answer = question['answer']
                    response_data['__label__' + str(topicId)] = answer['description']
            train_file.write(train_data)
            response_file.write(json.dumps(response_data))
            train_file.close()
            response_file.close()
            model = fasttext.train_supervised(input=train_file_name, lr=1.0, epoch=25, wordNgrams=3)
            model_file_name = os.path.join(os.getcwd(), 'files/models/' + languageCode + '.bin')
            createFile(model_file_name)
            model.save_model(model_file_name)