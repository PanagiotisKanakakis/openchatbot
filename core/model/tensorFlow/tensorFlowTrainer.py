import json
import pickle
import random

import nltk
import numpy as np
import tensorflow as tf
import tflearn
from chatterbot.trainers import Trainer
from nltk.stem.lancaster import LancasterStemmer


class ChatterBotTensorFlowTrainer(Trainer):
    """
    Allows the chat bot to be trained using data from the
    ChatterBot dialog corpus.
    """

    model = None

    def train(self, *corpus_paths):

        for file_path in corpus_paths:
            words, classes, documents, responses = self.getTrainingData(file_path)
            train_x, train_y = self.transformDataToModelFormat(words, classes, documents)
            self.trainModel(train_x, train_y)
            pickle.dump(
                {'words': words, 'classes': classes, 'responses': responses, 'train_x': train_x, 'train_y': train_y},
                open("training_data", "wb"))

    def getTrainingData(self, *corpus_path):
        stemmer = LancasterStemmer()
        counter = 0
        with open(*corpus_path) as json_data:
            intents = json.load(json_data)
            words = []
            classes = []
            responses = []
            documents = []
            ignore_words = ['?']
            # loop through each sentence in our intents patterns
            for QnA in intents['conversations']:
                question = QnA[0]
                answer = QnA[1]
                # tokenize each word in the sentence
                w = nltk.word_tokenize(question)
                # add to our words list
                words.extend(w)
                # add to documents in our corpus
                documents.append((w, '__label__QnA' + str(counter)))
                responses.append(answer)
                # add to our classes list
                if '__label__QnA' + str(counter) not in classes:
                    print('__label__QnA' + str(counter), question)
                    classes.append('__label__QnA' + str(counter))
                counter += 1

            # stem and lower each word and remove duplicates
            words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
            words = sorted(list(set(words)))
            # remove duplicates
            classes = sorted(list(set(classes)))
            return words, classes, documents, responses

    def transformDataToModelFormat(self, words, classes, documents):
        # create our training data
        training = []
        output = []
        # create an empty array for our output
        output_empty = [0] * len(classes)
        stemmer = LancasterStemmer()

        # training set, bag of words for each sentence
        for doc in documents:
            # initialize our bag of words
            bag = []
            # list of tokenized words for the pattern
            pattern_words = doc[0]
            # stem each word
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            # create our bag of words array
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            # output is a '0' for each tag and '1' for current tag
            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1

            training.append([bag, output_row])

        # shuffle our features and turn into np.array
        random.shuffle(training)
        training = np.array(training)

        # create train and test lists
        train_x = list(training[:, 0])
        train_y = list(training[:, 1])
        return train_x, train_y

    @classmethod
    def trainModel(cls, train_x, train_y):
        # reset underlying graph data
        tf.reset_default_graph()
        # Build neural network
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        # Define model and setup tensorboard
        # global model
        cls.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        # Start training (apply gradient descent algorithm)
        cls.model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=False)
        cls.model.save('model.tflearn')

    @classmethod
    def get_model(cls, data):
        if cls.model is None:
            # reset underlying graph data
            tf.reset_default_graph()
            # Build neural network
            net = tflearn.input_data(shape=[None, len(data['train_x'][0])])
            net = tflearn.fully_connected(net, 8)
            net = tflearn.fully_connected(net, 8)
            net = tflearn.fully_connected(net, len(data['train_y'][0]), activation='softmax')
            net = tflearn.regression(net)

            # Define model and setup tensorboard
            cls.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
            cls.model.load('./model.tflearn')
        return cls.model
