import json

import fasttext
from chatterbot.trainers import Trainer


class ChatterBotFastTextTrainer(Trainer):
    """
    Allows the chat bot to be trained using data from the
    ChatterBot dialog corpus.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.model = None
        self.model_name = 'fastText-model'
        self.train_file_name = 'train_data_fastText.txt'
        self.response_file_name = 'resposes_fastText.json'

    def train(self, *corpus_paths):
        for file_path in corpus_paths:
            self.modifyTrainingData(file_path)
            self.model = fasttext.train_supervised(input=self.train_file_name, lr=1.0, epoch=25, wordNgrams=3)
            self.model.save_model(self.model_name + '.bin')
            # self.chatbot.storage.create_many(statements_to_create)

    def modifyTrainingData(self, *corpus_path):
        train_data = ''
        response_data = {}
        train_file = open(self.train_file_name, 'w')
        response_file = open(self.response_file_name, 'w')

        with open(*corpus_path, "r", encoding='utf-8') as json_data:
            intents = json.load(json_data)
            for QnA in intents['conversations']:
                for pattern in QnA['patterns']:
                    train_data += '__label__' + QnA['tag'] + ' ' + pattern + '\n'
                response_data['__label__' + QnA['tag']] = QnA['responses'][0]

            train_file.write(train_data)
            response_file.write(json.dumps(response_data))
            train_file.close()
            response_file.close()
