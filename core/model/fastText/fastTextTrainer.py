import json

import fasttext
from chatterbot.trainers import Trainer


class ChatterBotFastTextTrainer(Trainer):
    """
    Allows the chat bot to be trained using data from the
    ChatterBot dialog corpus.
    """

    model = None
    model_name = 'fastText-model'
    train_file_name = 'train_data_fastText.txt'
    response_file_name = 'resposes_fastText.json'

    @classmethod
    def train(cls, *corpus_paths):
        for file_path in corpus_paths:
            cls.modifyTrainingData(file_path)
            model = fasttext.train_supervised(input=cls.train_file_name, lr=1.0, epoch=25, wordNgrams=2)
            model.save_model(cls.model_name + '.bin')

    @classmethod
    def modifyTrainingData(cls, *corpus_path):
        train_data = ''
        response_data = {}
        train_file = open(cls.train_file_name, 'w')
        response_file = open(cls.response_file_name, 'w')

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

    @classmethod
    def get_model(cls):
        if cls.model is None:
            cls.model = fasttext.load_model(cls.model_name + '.bin')
        return cls.model
